"""A lightweight, local vector store backed by JSON on disk."""

import json
import math
from pathlib import Path

from app.core.config import settings
from app.core.logger import get_logger
from app.rag.chunking import Chunk
from app.rag.embeddings import EmbeddingModel, get_embedding_model

logger = get_logger(__name__)

COLLECTION_NAME = "poultry_disease_knowledge_base"


class VectorStore:
    def __init__(
        self,
        persist_directory: str = settings.chroma_db_path,
        embedding_model: EmbeddingModel | None = None,
    ):
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.embedding_model = embedding_model or get_embedding_model()
        self._client = None
        self._collection = None
        self._documents: list[dict] = []
        self._store_path = self.persist_directory / f"{COLLECTION_NAME}.json"
        self._load()

    def _load(self) -> None:
        if self._store_path.exists():
            with self._store_path.open("r", encoding="utf-8") as handle:
                self._documents = json.load(handle)

    def _save(self) -> None:
        with self._store_path.open("w", encoding="utf-8") as handle:
            json.dump(self._documents, handle, indent=2)

    def add_chunks(self, chunks: list[Chunk]) -> None:
        """Embed and upsert a batch of chunks into the collection."""
        if not chunks:
            return

        texts = [chunk.text for chunk in chunks]
        vectors = self.embedding_model.embed_texts(texts)
        ids = [chunk.metadata.get("chunk_id", f"chunk-{index}") for index, chunk in enumerate(chunks)]

        for chunk, vector, chunk_id in zip(chunks, vectors, ids, strict=False):
            record = {
                "id": chunk_id,
                "text": chunk.text,
                "metadata": chunk.metadata,
                "embedding": vector,
            }
            existing = {item["id"]: item for item in self._documents}
            existing[chunk_id] = record
            self._documents = list(existing.values())

        self._save()

    def similarity_search(self, query: str, top_k: int = settings.retriever_top_k) -> list[dict]:
        """Embed a query and return the top_k most similar chunks based on semantic similarity."""
        if not self._documents:
            return []

        query_vector = self.embedding_model.embed_query(query)
        results: list[dict] = []
        for document in self._documents:
            score = self._cosine_similarity(query_vector, document["embedding"])
            results.append(
                {
                    "text": document["text"],
                    "metadata": document["metadata"],
                    "score": round(score, 6),
                }
            )

        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:top_k]

    def collection_count(self) -> int:
        """Return how many chunks are currently indexed."""
        return len(self._documents)

    @staticmethod
    def _cosine_similarity(left: list[float], right: list[float]) -> float:
        if not left or not right:
            return 0.0
        dot_product = sum(a * b for a, b in zip(left, right, strict=False))
        left_norm = math.sqrt(sum(value * value for value in left))
        right_norm = math.sqrt(sum(value * value for value in right))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return dot_product / (left_norm * right_norm)
