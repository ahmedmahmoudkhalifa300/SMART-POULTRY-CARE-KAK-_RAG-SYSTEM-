"""
FastAPI routes for uploading new PDF documents into the knowledge base
(admin/ingestion side, separate from the end-user chat/image endpoints).
"""

from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel

from app.core.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/upload", tags=["upload"])


class UploadResponse(BaseModel):
    filename: str
    chunks_indexed: int


@router.post("/pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)) -> UploadResponse:
    """
    Accepts a new PDF, saves it into data/pdfs/, and indexes it into
    ChromaDB so it becomes searchable by the chat endpoint.

    TODO:
    1. Validate file.content_type == "application/pdf".
    2. Save the upload to data/pdfs/{file.filename} (use app.core.utils.ensure_dir).
    3. raw_doc = app.rag.loader.load_pdf(saved_path)
    4. cleaned = app.rag.preprocessing.clean_text(raw_doc.text)
    5. chunks = app.rag.chunking.chunk_text(cleaned, raw_doc.metadata)
    6. app.rag.vector_store.VectorStore().add_chunks(chunks)
    7. return UploadResponse(filename=file.filename, chunks_indexed=len(chunks))
    """
    raise NotImplementedError
