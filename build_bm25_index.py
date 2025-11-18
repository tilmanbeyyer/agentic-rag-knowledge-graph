"""
Build BM25 index from existing database chunks.

This script builds a BM25 index from all chunks in the PostgreSQL database.
The index is saved to disk and will be automatically loaded by the agent.

Run this script after ingesting documents to enable BM25 and hybrid search.
"""

import asyncio
import logging
from pathlib import Path

from agent.bm25_utils import rebuild_bm25_index
from agent.db_utils import initialize_database, close_database

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Build the BM25 index."""
    logger.info("Starting BM25 index build process...")

    # Check if data directory exists
    data_dir = Path("data/bm25_index")
    if data_dir.exists():
        logger.info(f"Existing BM25 index found at {data_dir}")
        response = input("Rebuild index? This will overwrite the existing index. (y/n): ")
        if response.lower() != 'y':
            logger.info("Aborting index build.")
            return

    try:
        # Initialize database connection
        logger.info("Initializing database connection...")
        await initialize_database()

        # Build the index
        logger.info("Building BM25 index from database chunks...")
        logger.info("This may take a few minutes depending on the number of chunks...")
        success = await rebuild_bm25_index()

        if success:
            logger.info("✅ BM25 index built successfully!")
            logger.info(f"Index saved to: {data_dir}")
            logger.info("\nYou can now use BM25 and hybrid search in the agent:")
            logger.info("- bm25_search: For keyword-based lexical search")
            logger.info("- hybrid_search: For combined semantic + keyword search")
        else:
            logger.error("❌ Failed to build BM25 index")
            logger.error("Make sure you have run document ingestion first")

    except Exception as e:
        logger.error(f"Error building BM25 index: {e}")
        raise
    finally:
        # Close database connection
        await close_database()
        logger.info("Database connection closed")


if __name__ == "__main__":
    asyncio.run(main())
