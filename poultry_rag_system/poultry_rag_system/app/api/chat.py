"""FastAPI routes for the text Q&A (RAG) service."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.logger import get_logger
from app.state import state

logger = get_logger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    question: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]


def get_pipeline():
    """Get the RAG pipeline, waiting for warm-up if necessary."""
    # Wait for the pipeline to be ready (with a timeout)
    if not state.pipeline_ready.wait(timeout=20.0):
        raise RuntimeError("RAG pipeline warm-up timed out")
    if state.pipeline is None:
        raise RuntimeError("RAG pipeline failed to warm up")
    return state.pipeline


@router.get("/")
def chat_info():
    """Return a helpful message when accessed via browser (GET)."""
    return {
        "message": "This is the chat API endpoint. Use POST with a JSON body containing 'question' and 'session_id'.",
        "example": {"question": "What are common poultry diseases?", "session_id": "optional-session-id"},
        "docs": "/docs",
    }


@router.post("/", response_model=ChatResponse)
def ask_question(payload: ChatRequest) -> ChatResponse:
    """Accept a user question and return an answer grounded in the knowledge base."""
    try:
        session_id = payload.session_id or "default"
        pipe = get_pipeline()
        result = pipe.answer_question(payload.question, session_id=session_id)

        try:
            from app.database.history import log_chat
            log_chat(payload.question, result["answer"])
        except Exception as db_exc:
            logger.warning("Failed to log chat to database: %s", db_exc)

        return ChatResponse(**result)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Chat request failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
