"""
One-off / repeatable CLI script to (re)index all PDFs in data/pdfs/ into
ChromaDB. Run this whenever new documents are added to the knowledge base.

Usage:
    python scripts/index_pdfs.py
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.core.logger import get_logger
from app.services.knowledge_base_service import KnowledgeBaseService

logger = get_logger(__name__)


def main() -> None:
    service = KnowledgeBaseService()
    summary = service.ingest_directory("data/pdfs")
    logger.info(f"Ingestion complete: {summary}")


if __name__ == "__main__":
    main()
