"""Orchestrates the ingestion flow for the local knowledge base."""

from pathlib import Path

from app.core.logger import get_logger
from app.rag.chunking import chunk_text
from app.rag.loader import load_document
from app.rag.preprocessing import clean_text
from app.rag.vector_store import VectorStore

logger = get_logger(__name__)


class KnowledgeBaseService:
    def __init__(self, vector_store: VectorStore | None = None):
        self.vector_store = vector_store or VectorStore()

    def ingest_document(self, path: str | Path) -> int:
        """Ingest a single document (PDF/DOCX) into the vector store and return chunk count."""
        raw_doc = load_document(path)
        if raw_doc is None or not raw_doc.text.strip():
            return 0
        cleaned = clean_text(raw_doc.text)
        chunks = chunk_text(cleaned, raw_doc.metadata)
        self.vector_store.add_chunks(chunks)
        return len(chunks)

    def ingest_directory(self, directory: str | Path = "data/pdfs") -> dict:
        """Ingest every PDF and DOCX in a directory and return a summary dict."""
        data_dir = Path(directory)
        if not data_dir.exists():
            return {"files_processed": 0, "chunks_indexed": 0, "errors": []}

        files_processed = 0
        chunks_indexed = 0
        errors: list[str] = []
        for path in sorted(data_dir.iterdir()):
            if path.suffix.lower() not in {".pdf", ".docx"}:
                continue
            try:
                files_processed += 1
                chunks_indexed += self.ingest_document(path)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{path.name}: {exc}")

        return {"files_processed": files_processed, "chunks_indexed": chunks_indexed, "errors": errors}
