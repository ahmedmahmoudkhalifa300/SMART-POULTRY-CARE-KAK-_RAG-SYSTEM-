"""Lightweight text embedding wrapper used by the local vector store."""

import math
import os
from typing import Any

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

if settings.hf_token:
    os.environ["HF_TOKEN"] = settings.hf_token


class EmbeddingModel:
    """Wrapper around sentence-transformers for semantic embeddings."""

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")
        self.dimension = 384
        self._model = None

    def _get_model(self) -> Any:
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer  # noqa: PLC0415
            except ImportError as exc:
                raise RuntimeError(
                    "sentence-transformers is required for semantic search. "
                    "Install it with: pip install sentence-transformers"
                ) from exc
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of chunk texts. Returns one vector per input string."""
        model = self._get_model()
        embeddings = model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        """Embed a single user query string for similarity search."""
        model = self._get_model()
        embedding = model.encode([query], normalize_embeddings=True)
        return embedding[0].tolist()


def get_embedding_model() -> EmbeddingModel:
    """Factory so callers don't need to know the concrete class/config."""
    return EmbeddingModel()
