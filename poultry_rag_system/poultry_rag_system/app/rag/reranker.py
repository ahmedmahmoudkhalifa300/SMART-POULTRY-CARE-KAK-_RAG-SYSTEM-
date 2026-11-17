"""A lightweight reranking stage that keeps the most relevant chunks first."""

import math
from collections import Counter
from typing import Any

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class Reranker:
    def __init__(self):
        self._model = None

    def _get_model(self) -> Any:
        if self._model is None:
            try:
                from sentence_transformers import CrossEncoder  # noqa: PLC0415
            except ImportError as exc:
                raise RuntimeError(
                    "sentence-transformers is required for cross-encoder reranking. "
                    "Install it with: pip install sentence-transformers"
                ) from exc
            self._model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        return self._model

    def rerank(self, query: str, candidates: list[dict], top_k: int = settings.reranker_top_k) -> list[dict]:
        """
        Re-score candidates using a cross-encoder model for better semantic relevance.
        
        This improves over simple lexical/BM25 scoring by:
        1. Using a cross-encoder that considers query-document pairs jointly
        2. Better handling of semantic similarity
        3. More accurate relevance scoring
        """
        if not candidates:
            return []

        if len(candidates) <= top_k:
            return candidates[:top_k]

        try:
            model = self._get_model()
            pairs = [(query, candidate.get("text", "")) for candidate in candidates]
            scores = model.predict(pairs)
            
            reranked = []
            for candidate, score in zip(candidates, scores):
                candidate_with_score = dict(candidate)
                candidate_with_score["score"] = round(float(score), 6)
                reranked.append(candidate_with_score)
            
            reranked.sort(key=lambda item: item.get("score", 0.0), reverse=True)
            return reranked[:top_k]
        except Exception as exc:  # noqa: BLE001
            logger.warning("Cross-encoder reranking failed, falling back to original order: %s", exc)
            return candidates[:top_k]
