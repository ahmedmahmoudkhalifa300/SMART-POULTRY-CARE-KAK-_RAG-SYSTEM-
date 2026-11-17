"""
FastAPI application entrypoint.

Run with:
    uvicorn app.main:app --reload
"""

import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api import chat, image, upload
from app.core.logger import get_logger
from app.rag import prompt_builder

logger = get_logger(__name__)


def warm_up_rag() -> None:
    """Warm up RAGPipeline models and ChromaDB on startup in a background thread."""
    logger.info("Starting background RAG warm-up...")
    from app.state import state
    try:
        from app.rag.pipeline import RAGPipeline
        # Initialize pipeline (loads Retriever, ChromaDB, and Embedding model)
        pipeline = RAGPipeline()
        # Run a simple pre-flight query to compile/cache tokenizers, embeddings, and database connection
        logger.info("Running pre-flight RAG query...")
        pipeline.answer_question("test warm up query", session_id="warmup_session")
        state.pipeline = pipeline
        logger.info("RAG system warmed up successfully and ready for queries!")
    except Exception as exc:
        logger.exception("Failed to warm up RAG pipeline: %s", exc)
    finally:
        state.pipeline_ready.set()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the database tables
    from app.database.history import init_db
    try:
        init_db()
        logger.info("Database initialized successfully.")
    except Exception as exc:
        logger.exception("Failed to initialize database: %s", exc)

    # Run RAG warm-up in a separate background thread so we don't block server startup
    warmup_thread = threading.Thread(target=warm_up_rag, daemon=True)
    warmup_thread.start()
    yield


app = FastAPI(
    title="Poultry Disease RAG System",
    description=(
        "AI-powered assistant combining Retrieval-Augmented Generation and "
        "Computer Vision to answer poultry disease questions and diagnose "
        "diseases from images."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(image.router)
app.include_router(upload.router)


@app.get("/health")
def health_check() -> dict:
    """Basic liveness check."""
    return {"status": "ok"}


@app.get("/")
def root() -> RedirectResponse:
    """Redirect root to API docs."""

    return RedirectResponse(url="/docs")
