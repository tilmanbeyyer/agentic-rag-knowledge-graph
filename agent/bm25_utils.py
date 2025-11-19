"""
BM25 search utilities using bm25s library.

This module provides BM25-based lexical search capabilities to complement
the semantic vector search in the RAG system.
"""

import os
import logging
import pickle
import json
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

import bm25s
from dotenv import load_dotenv

from .db_utils import db_pool

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Global BM25 index and corpus storage
_bm25_index = None
_corpus_data = None  # Stores chunk metadata (id, document_id, etc.)
_index_path = Path("data/bm25_index")


class BM25Index:
    """
    Manages BM25 index for lexical search.

    The index is built from chunks in the PostgreSQL database and cached
    to disk for fast loading.
    """

    def __init__(self, index_dir: str = "data/bm25_index"):
        """
        Initialize BM25 index manager.

        Args:
            index_dir: Directory to store the BM25 index files
        """
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)

        # BM25S creates these files automatically
        self.corpus_file = self.index_dir / "corpus_data.pkl"

        self.retriever: Optional[bm25s.BM25] = None
        self.corpus_data: List[Dict[str, Any]] = []

    async def build_index(self, force_rebuild: bool = False) -> bool:
        """
        Build BM25 index from database chunks.

        Args:
            force_rebuild: If True, rebuild even if index exists

        Returns:
            True if index was built successfully
        """
        # Check if index already exists (check for corpus file as marker)
        if not force_rebuild and self.corpus_file.exists():
            logger.info("BM25 index already exists, loading from disk")
            return await self.load_index()

        logger.info("Building BM25 index from database chunks...")

        try:
            # Fetch all chunks from database
            async with db_pool.acquire() as conn:
                results = await conn.fetch("""
                    SELECT
                        c.id::text AS chunk_id,
                        c.document_id::text,
                        c.content,
                        c.chunk_index,
                        c.metadata,
                        d.title AS document_title,
                        d.source AS document_source
                    FROM chunks c
                    JOIN documents d ON c.document_id = d.id
                    ORDER BY c.document_id, c.chunk_index
                """)

            if not results:
                logger.warning("No chunks found in database")
                return False

            # Extract corpus and metadata
            corpus_texts = []
            self.corpus_data = []

            for row in results:
                corpus_texts.append(row["content"])

                # Parse metadata JSON string to dict (like db_utils.py does)
                # Reason: PostgreSQL JSONB returns as string, but ChunkResult expects dict
                metadata = row["metadata"]
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except (json.JSONDecodeError, TypeError):
                        logger.warning(f"Failed to parse metadata for chunk {row['chunk_id']}, using empty dict")
                        metadata = {}

                self.corpus_data.append({
                    "chunk_id": row["chunk_id"],
                    "document_id": row["document_id"],
                    "content": row["content"],
                    "chunk_index": row["chunk_index"],
                    "metadata": metadata,
                    "document_title": row["document_title"],
                    "document_source": row["document_source"]
                })

            logger.info(f"Building BM25 index with {len(corpus_texts)} chunks")

            # Tokenize corpus using bm25s tokenizer
            corpus_tokens = bm25s.tokenize(corpus_texts, stopwords="en")

            # Create BM25 retriever
            self.retriever = bm25s.BM25()
            self.retriever.index(corpus_tokens)

            # Save index to disk
            await self.save_index()

            logger.info("BM25 index built and saved successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to build BM25 index: {e}")
            return False

    async def save_index(self):
        """Save BM25 index and corpus data to disk."""
        try:
            # Save the BM25 retriever
            self.retriever.save(str(self.index_dir))

            # Save corpus data
            with open(self.corpus_file, 'wb') as f:
                pickle.dump(self.corpus_data, f)

            logger.info(f"BM25 index saved to {self.index_dir}")

        except Exception as e:
            logger.error(f"Failed to save BM25 index: {e}")
            raise

    async def load_index(self) -> bool:
        """
        Load BM25 index from disk.

        Returns:
            True if loaded successfully
        """
        try:
            if not self.corpus_file.exists():
                logger.warning("BM25 corpus data file not found")
                return False

            # Load the BM25 retriever (it checks for its own files)
            self.retriever = bm25s.BM25.load(str(self.index_dir), mmap=False)

            # Load corpus data
            with open(self.corpus_file, 'rb') as f:
                self.corpus_data = pickle.load(f)

            logger.info(f"BM25 index loaded with {len(self.corpus_data)} chunks")
            return True

        except Exception as e:
            logger.error(f"Failed to load BM25 index: {e}")
            return False

    async def search(
        self,
        query: str,
        limit: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Search using BM25 algorithm.

        Args:
            query: Search query text
            limit: Maximum number of results to return

        Returns:
            List of matching chunks with BM25 scores
        """
        if self.retriever is None:
            # Try to load index first
            loaded = await self.load_index()
            if not loaded:
                # Build index if it doesn't exist
                await self.build_index()

            if self.retriever is None:
                logger.error("BM25 index not available")
                return []

        # Handle empty corpus
        if not self.corpus_data:
            logger.warning("BM25 corpus is empty")
            return []

        try:
            # Clamp limit to corpus size to avoid bm25s errors
            # Reason: bm25s raises an error if k > corpus size
            actual_limit = min(limit, len(self.corpus_data))
            if actual_limit < limit:
                logger.debug(
                    f"Clamped BM25 search limit from {limit} to {actual_limit} "
                    f"(corpus size: {len(self.corpus_data)})"
                )

            # Tokenize query
            query_tokens = bm25s.tokenize(query, stopwords="en")

            # Search
            results, scores = self.retriever.retrieve(
                query_tokens,
                k=actual_limit
            )

            # Format results
            search_results = []
            for idx, score in zip(results[0], scores[0]):
                if idx < len(self.corpus_data):
                    chunk_data = self.corpus_data[idx]
                    search_results.append({
                        "chunk_id": chunk_data["chunk_id"],
                        "document_id": chunk_data["document_id"],
                        "content": chunk_data["content"],
                        "score": float(score),
                        "metadata": chunk_data["metadata"],
                        "document_title": chunk_data["document_title"],
                        "document_source": chunk_data["document_source"]
                    })

            return search_results

        except Exception as e:
            logger.error(f"BM25 search failed: {e}")
            return []


# Global BM25 index instance
_bm25_index_instance: Optional[BM25Index] = None


async def get_bm25_index() -> BM25Index:
    """
    Get or create the global BM25 index instance.

    Returns:
        BM25Index instance
    """
    global _bm25_index_instance

    if _bm25_index_instance is None:
        _bm25_index_instance = BM25Index()
        # Try to load existing index, build if not available
        loaded = await _bm25_index_instance.load_index()
        if not loaded:
            logger.info("BM25 index not found, building new index...")
            await _bm25_index_instance.build_index()

    return _bm25_index_instance


async def bm25_search(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Perform BM25 lexical search.

    Args:
        query: Search query text
        limit: Maximum number of results

    Returns:
        List of matching chunks with BM25 scores
    """
    index = await get_bm25_index()
    return await index.search(query, limit)


async def rebuild_bm25_index() -> bool:
    """
    Force rebuild of the BM25 index from database.

    Returns:
        True if rebuild successful
    """
    index = await get_bm25_index()
    return await index.build_index(force_rebuild=True)


async def hybrid_bm25_vector_search(
    query: str,
    vector_results: List[Dict[str, Any]],
    bm25_weight: float = 0.3,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Combine BM25 and vector search results with weighted scoring.

    Args:
        query: Search query text
        vector_results: Results from vector search (with 'similarity' scores)
        bm25_weight: Weight for BM25 scores (0-1), vector gets (1 - bm25_weight)
        limit: Maximum number of results

    Returns:
        Combined results sorted by weighted score
    """
    # Perform BM25 search
    bm25_results = await bm25_search(query, limit=limit * 2)

    # Create score dictionaries for easy lookup
    bm25_scores = {r["chunk_id"]: r["score"] for r in bm25_results}
    vector_scores = {r["chunk_id"]: r.get("similarity", 0) for r in vector_results}

    # Normalize scores to 0-1 range
    max_bm25 = max(bm25_scores.values()) if bm25_scores else 1.0
    max_vector = max(vector_scores.values()) if vector_scores else 1.0

    # Combine all unique chunks
    all_chunk_ids = set(bm25_scores.keys()) | set(vector_scores.keys())

    combined_results = []
    chunk_data_map = {r["chunk_id"]: r for r in bm25_results + vector_results}

    for chunk_id in all_chunk_ids:
        norm_bm25 = bm25_scores.get(chunk_id, 0) / max_bm25
        norm_vector = vector_scores.get(chunk_id, 0) / max_vector

        combined_score = (
            norm_bm25 * bm25_weight +
            norm_vector * (1 - bm25_weight)
        )

        if chunk_id in chunk_data_map:
            result = chunk_data_map[chunk_id].copy()
            result["combined_score"] = combined_score
            result["bm25_score"] = bm25_scores.get(chunk_id, 0)
            result["vector_score"] = vector_scores.get(chunk_id, 0)
            combined_results.append(result)

    # Sort by combined score and limit
    combined_results.sort(key=lambda x: x["combined_score"], reverse=True)
    return combined_results[:limit]
