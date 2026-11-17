"""
Centralized configuration for the Poultry Disease RAG System.

Rules:
- Never hardcode API keys or secrets in this file.
- All sensitive values are loaded at runtime from Streamlit Secrets
  (st.secrets), falling back to environment variables so the same code
  works when called from a plain FastAPI process (no Streamlit context).
- Import `settings` from this module everywhere else in the app instead
  of reading secrets directly.
"""

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env", override=False)


def _resolve_path(value: str | None, default: str) -> str:
    """Resolve relative paths against the project root when needed."""
    if not value:
        return str(PROJECT_ROOT / default)
    if os.path.isabs(value):
        return value
    return str(PROJECT_ROOT / value)


def _get_secret(key: str, default: str | None = None) -> str | None:
    """
    Look up a config value, preferring Streamlit Secrets when available
    (e.g. when running under `streamlit run`), and falling back to
    environment variables (e.g. when running under `uvicorn`/FastAPI,
    or in CI).
    """
    try:
        import streamlit as st  # noqa: PLC0415
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        # Not running inside a Streamlit context, or secrets.toml missing.
        pass
    return os.environ.get(key, default)


@dataclass(frozen=True)
class Settings:
    openrouter_api_key: str | None
    openrouter_model: str
    google_api_key: str | None
    hf_token: str | None
    chroma_db_path: str
    model_path: str
    tessdata_prefix: str

    # RAG tuning knobs — TODO: tune these once real documents are indexed.
    chunk_size: int = 450
    chunk_overlap: int = 200
    retriever_top_k: int = 5
    reranker_top_k: int = 3

    # Vision tuning knobs — MUST match the trained model's output layer exactly.
    image_size: tuple[int, int] = (224, 224)
    disease_classes: tuple[str, ...] = (
        "Coccidiosis",
        "Healthy",
        "New Castle Disease",
        "Salmonella",
    )


@lru_cache
def get_settings() -> Settings:
    """Load settings once per process and cache them."""
    return Settings(
        openrouter_api_key=_get_secret("OPENROUTER_API_KEY"),
        openrouter_model=_get_secret("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
        google_api_key=_get_secret("GOOGLE_API_KEY"),
        hf_token=_get_secret("HF_TOKEN"),
        chroma_db_path=_resolve_path(_get_secret("CHROMA_DB_PATH", "./vector_db"), "./vector_db"),
        model_path=_resolve_path(_get_secret("MODEL_PATH", "./models/poultry_classifier.keras"), "./models/poultry_classifier.keras"),
        tessdata_prefix=_resolve_path(_get_secret("TESSDATA_PREFIX", "./tessdata"), "./tessdata"),
    )


settings = get_settings()
