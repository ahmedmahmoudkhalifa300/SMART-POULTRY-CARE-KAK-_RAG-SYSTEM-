import unittest

from app.rag.chunking import chunk_text
from app.rag.embeddings import EmbeddingModel
from app.rag.pipeline import RAGPipeline
from app.rag.preprocessing import clean_text
from app.rag.vector_store import VectorStore


class RAGPipelineTests(unittest.TestCase):
    def test_clean_text_normalizes_hyphenated_line_breaks(self) -> None:
        raw = "coccidio-\nsis is a disease"
        cleaned = clean_text(raw)
        self.assertIn("coccidiosis", cleaned)
        self.assertNotIn("\n", cleaned)

    def test_chunk_text_returns_overlapping_chunks(self) -> None:
        text = "A long piece of text that should be split into multiple chunks for retrieval. " * 3
        chunks = chunk_text(text, {"source": "sample.pdf"}, chunk_size=40, chunk_overlap=10)
        self.assertGreaterEqual(len(chunks), 2)
        self.assertTrue(all(chunk.text for chunk in chunks))

    def test_embedding_model_returns_vectors(self) -> None:
        model = EmbeddingModel()
        vectors = model.embed_texts(["poultry disease", "newcastle disease"])
        self.assertEqual(len(vectors), 2)
        self.assertTrue(all(len(vector) > 0 for vector in vectors))

    def test_vector_store_round_trip(self) -> None:
        store = VectorStore(persist_directory="./tmp_test_vector_db")
        chunks = chunk_text("Newcastle disease causes respiratory issues in poultry.", {"source": "sample.pdf"}, chunk_size=40, chunk_overlap=5)
        store.add_chunks(chunks)
        results = store.similarity_search("poultry respiratory disease", top_k=1)
        self.assertTrue(results)

    def test_pipeline_returns_answer_and_sources(self) -> None:
        pipeline = RAGPipeline()
        result = pipeline.answer_question("How do I prevent coccidiosis in poultry?")
        self.assertIn("answer", result)
        self.assertIn("sources", result)

    def test_fallback_uses_retrieved_context_when_llm_is_unavailable(self) -> None:
        pipeline = RAGPipeline()
        pipeline._llm_client = None
        context_chunks = [
            {
                "text": "Newcastle disease can cause respiratory signs, depression, and sudden death in poultry.",
                "metadata": {"source": "sample.pdf", "page": 1},
            }
        ]

        response = pipeline._call_llm(
            [{"role": "user", "content": "What are symptoms of Newcastle disease?"}],
            context_chunks=context_chunks,
            question="What are symptoms of Newcastle disease?",
        )

        self.assertIn("الذكاء الاصطناعي غير متاح مؤقتاً", response)
        self.assertIn("newcastle", response.lower())


if __name__ == "__main__":
    unittest.main()
