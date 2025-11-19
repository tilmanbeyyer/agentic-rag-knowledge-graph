"""
Tests for BM25 search utilities.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from pathlib import Path
import pickle

from agent.bm25_utils import (
    BM25Index,
    get_bm25_index,
    bm25_search,
    rebuild_bm25_index,
    hybrid_bm25_vector_search
)


@pytest.fixture
def mock_db_pool():
    """Mock database pool."""
    with patch('agent.bm25_utils.db_pool') as mock_pool:
        mock_conn = AsyncMock()
        mock_pool.acquire.return_value.__aenter__.return_value = mock_conn
        yield mock_conn


@pytest.fixture
def sample_chunks():
    """Sample chunks for testing."""
    return [
        {
            "chunk_id": "chunk-1",
            "document_id": "doc-1",
            "content": "This is a test document about Python programming",
            "chunk_index": 0,
            "metadata": {},
            "document_title": "Python Guide",
            "document_source": "test.md"
        },
        {
            "chunk_id": "chunk-2",
            "document_id": "doc-1",
            "content": "Python is a popular programming language",
            "chunk_index": 1,
            "metadata": {},
            "document_title": "Python Guide",
            "document_source": "test.md"
        },
        {
            "chunk_id": "chunk-3",
            "document_id": "doc-2",
            "content": "Machine learning algorithms are fascinating",
            "chunk_index": 0,
            "metadata": {},
            "document_title": "ML Basics",
            "document_source": "ml.md"
        }
    ]


@pytest.fixture
def bm25_index(tmp_path, sample_chunks):
    """Create a BM25 index instance with temp directory."""
    index = BM25Index(index_dir=str(tmp_path / "bm25_test"))
    return index


def create_mock_record(data):
    """Create a mock record that supports dict-like access."""
    mock_record = Mock()
    # Make the mock support item access like a dict
    mock_record.__getitem__ = lambda _, key: data[key]
    return mock_record


@pytest.mark.asyncio
async def test_build_index_success(bm25_index, mock_db_pool, sample_chunks):
    """Test successful BM25 index building."""
    # Mock database results - create proper mock records that support dict-like access
    mock_records = [create_mock_record(chunk) for chunk in sample_chunks]
    mock_db_pool.fetch.return_value = mock_records

    # Build index
    result = await bm25_index.build_index(force_rebuild=True)

    assert result is True
    assert bm25_index.retriever is not None
    assert len(bm25_index.corpus_data) == 3
    assert bm25_index.corpus_data[0]["chunk_id"] == "chunk-1"


@pytest.mark.asyncio
async def test_build_index_no_chunks(bm25_index, mock_db_pool):
    """Test building index with no chunks."""
    # Mock empty database results
    mock_db_pool.fetch.return_value = []

    # Build index
    result = await bm25_index.build_index(force_rebuild=True)

    assert result is False
    assert bm25_index.retriever is None


@pytest.mark.asyncio
async def test_save_and_load_index(bm25_index, mock_db_pool, sample_chunks):
    """Test saving and loading BM25 index."""
    # Mock database results - create proper mock records that support dict-like access
    mock_records = [create_mock_record(chunk) for chunk in sample_chunks]
    mock_db_pool.fetch.return_value = mock_records

    # Build and save index
    await bm25_index.build_index(force_rebuild=True)

    # Create new index instance and load
    new_index = BM25Index(index_dir=bm25_index.index_dir)
    result = await new_index.load_index()

    assert result is True
    assert new_index.retriever is not None
    assert len(new_index.corpus_data) == 3


@pytest.mark.asyncio
async def test_search_basic(bm25_index, mock_db_pool, sample_chunks):
    """Test basic BM25 search."""
    # Mock database results - create proper mock records that support dict-like access
    mock_records = [create_mock_record(chunk) for chunk in sample_chunks]
    mock_db_pool.fetch.return_value = mock_records

    # Build index
    await bm25_index.build_index(force_rebuild=True)

    # Search for "Python"
    results = await bm25_index.search("Python programming", limit=2)

    assert len(results) <= 2
    assert len(results) > 0
    assert "chunk_id" in results[0]
    assert "score" in results[0]
    assert results[0]["score"] >= 0


@pytest.mark.asyncio
async def test_search_no_index(bm25_index):
    """Test search when index doesn't exist."""
    # Try to search without building index first
    # The function should try to load/build automatically
    with patch.object(bm25_index, 'load_index', return_value=False):
        with patch.object(bm25_index, 'build_index', return_value=False):
            results = await bm25_index.search("test query")
            assert results == []


@pytest.mark.asyncio
async def test_bm25_search_function(mock_db_pool, sample_chunks):
    """Test the bm25_search convenience function."""
    # Mock database results
    mock_records = [Mock(**chunk) for chunk in sample_chunks]
    mock_db_pool.fetch.return_value = mock_records

    # Mock the index retrieval
    with patch('agent.bm25_utils._bm25_index_instance', None):
        with patch('agent.bm25_utils.BM25Index') as MockBM25Index:
            mock_index = AsyncMock()
            mock_index.load_index.return_value = True
            mock_index.search.return_value = [sample_chunks[0]]
            MockBM25Index.return_value = mock_index

            results = await bm25_search("test query", limit=5)

            assert len(results) == 1
            mock_index.search.assert_called_once_with("test query", 5)


@pytest.mark.asyncio
async def test_rebuild_bm25_index(mock_db_pool, sample_chunks):
    """Test rebuilding BM25 index."""
    # Mock database results
    mock_records = [Mock(**chunk) for chunk in sample_chunks]
    mock_db_pool.fetch.return_value = mock_records

    with patch('agent.bm25_utils._bm25_index_instance', None):
        with patch('agent.bm25_utils.BM25Index') as MockBM25Index:
            mock_index = AsyncMock()
            mock_index.load_index.return_value = True
            mock_index.build_index.return_value = True
            MockBM25Index.return_value = mock_index

            result = await rebuild_bm25_index()

            assert result is True
            mock_index.build_index.assert_called_once_with(force_rebuild=True)


@pytest.mark.asyncio
async def test_hybrid_bm25_vector_search():
    """Test hybrid search combining BM25 and vector results."""
    # Sample vector results
    vector_results = [
        {
            "chunk_id": "chunk-1",
            "document_id": "doc-1",
            "content": "Test content 1",
            "similarity": 0.9,
            "metadata": {},
            "document_title": "Doc 1",
            "document_source": "doc1.md"
        },
        {
            "chunk_id": "chunk-2",
            "document_id": "doc-1",
            "content": "Test content 2",
            "similarity": 0.7,
            "metadata": {},
            "document_title": "Doc 1",
            "document_source": "doc1.md"
        }
    ]

    # Mock BM25 search results
    bm25_results = [
        {
            "chunk_id": "chunk-1",
            "document_id": "doc-1",
            "content": "Test content 1",
            "score": 5.0,
            "metadata": {},
            "document_title": "Doc 1",
            "document_source": "doc1.md"
        },
        {
            "chunk_id": "chunk-3",
            "document_id": "doc-2",
            "content": "Test content 3",
            "score": 3.0,
            "metadata": {},
            "document_title": "Doc 2",
            "document_source": "doc2.md"
        }
    ]

    with patch('agent.bm25_utils.bm25_search', return_value=bm25_results):
        results = await hybrid_bm25_vector_search(
            query="test query",
            vector_results=vector_results,
            bm25_weight=0.3,
            limit=5
        )

        # Should have results from both searches
        assert len(results) > 0
        # Should have combined scores
        assert "combined_score" in results[0]
        assert "bm25_score" in results[0]
        assert "vector_score" in results[0]
        # Results should be sorted by combined score
        if len(results) > 1:
            assert results[0]["combined_score"] >= results[1]["combined_score"]


@pytest.mark.asyncio
async def test_hybrid_search_with_overlapping_chunks():
    """Test hybrid search when same chunks appear in both results."""
    # Chunk-1 appears in both results
    vector_results = [
        {
            "chunk_id": "chunk-1",
            "content": "Test",
            "similarity": 0.8,
            "document_id": "doc-1",
            "metadata": {},
            "document_title": "Doc",
            "document_source": "doc.md"
        }
    ]

    bm25_results = [
        {
            "chunk_id": "chunk-1",
            "content": "Test",
            "score": 4.0,
            "document_id": "doc-1",
            "metadata": {},
            "document_title": "Doc",
            "document_source": "doc.md"
        }
    ]

    with patch('agent.bm25_utils.bm25_search', return_value=bm25_results):
        results = await hybrid_bm25_vector_search(
            query="test",
            vector_results=vector_results,
            bm25_weight=0.5,
            limit=5
        )

        # Should have only one result (the overlapping chunk)
        assert len(results) == 1
        # Should have combined scores from both methods
        assert results[0]["bm25_score"] > 0
        assert results[0]["vector_score"] > 0


@pytest.mark.asyncio
async def test_search_error_handling(bm25_index, mock_db_pool):
    """Test error handling in search."""
    # Mock database error
    mock_db_pool.fetch.side_effect = Exception("Database error")

    # Build should fail gracefully
    result = await bm25_index.build_index(force_rebuild=True)
    assert result is False


@pytest.mark.asyncio
async def test_search_limit_exceeds_corpus_size(bm25_index, mock_db_pool, sample_chunks):
    """Test search when requested limit exceeds corpus size."""
    # Use only 1 chunk to simulate small corpus
    single_chunk = [sample_chunks[0]]
    mock_records = [create_mock_record(single_chunk[0])]
    mock_db_pool.fetch.return_value = mock_records

    # Build index with just one chunk
    await bm25_index.build_index(force_rebuild=True)

    # Request 10 results when only 1 exists
    results = await bm25_index.search("Python programming", limit=10)

    # Should return 1 result without error
    assert len(results) == 1
    assert results[0]["chunk_id"] == "chunk-1"
    assert "score" in results[0]


@pytest.mark.asyncio
async def test_search_with_empty_corpus(bm25_index, mock_db_pool):
    """Test search with empty corpus."""
    # Build index with empty corpus
    mock_db_pool.fetch.return_value = []
    await bm25_index.build_index(force_rebuild=True)

    # Manually set empty corpus_data (since build returns False for empty corpus)
    bm25_index.corpus_data = []
    bm25_index.retriever = MagicMock()

    # Search should return empty list gracefully
    results = await bm25_index.search("test query", limit=10)

    assert results == []
