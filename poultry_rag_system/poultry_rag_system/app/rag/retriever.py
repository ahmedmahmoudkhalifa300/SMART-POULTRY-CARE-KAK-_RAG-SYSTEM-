"""Retrieval logic: takes a user query (or a predicted disease name from the
vision pipeline) and returns the most relevant knowledge-base chunks.
"""

from app.core.config import settings
from app.core.logger import get_logger
from app.rag.vector_store import VectorStore

logger = get_logger(__name__)


class Retriever:
    def __init__(self, vector_store: VectorStore | None = None):
        self.vector_store = vector_store or VectorStore()

    def retrieve(self, query: str, top_k: int = settings.retriever_top_k) -> list[dict]:
        """
        Return the top_k raw matches from the vector store for `query`.
        
        Uses pure semantic similarity search with sentence embeddings.
        """
        if not query:
            return []
        
        return self.vector_store.similarity_search(query, top_k=top_k)

    def retrieve_for_disease(self, disease_name: str, top_k: int = settings.retriever_top_k) -> list[dict]:
        """
        Specialized entry point used by the image-diagnosis flow: given a
        disease name predicted by the vision classifier, retrieve the most
        relevant knowledge-base chunks (symptoms/causes/treatment/prevention).
        """
        query = f"symptoms causes treatment prevention of {disease_name} in poultry"
        return self.retrieve(query, top_k=top_k)
