"""Top-level RAG orchestration: retrieve -> rerank -> build prompt -> call LLM."""

import re
import time
from functools import lru_cache
from typing import Any

from app.core.config import settings
from app.core.logger import get_logger
from app.rag.prompt_builder import build_diagnosis_prompt, build_qa_prompt
from app.rag.reranker import Reranker
from app.rag.retriever import Retriever
logger = get_logger(__name__)

MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 1.0
TRANSIENT_ERROR_PATTERNS = (
    "compaction worker",
    "empty response",
    "rate limit",
    "timeout",
    "service unavailable",
    "internal server error",
    "bad gateway",
    "gateway timeout",
)


def _is_transient_error(error: Exception) -> bool:
    message = str(error).lower()
    return any(pattern in message for pattern in TRANSIENT_ERROR_PATTERNS)


def _extract_relevant_section(text: str, question: str) -> str:
    """Extract only the relevant section from a full diagnosis response based on the question."""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['سبب', 'أسباب', 'لماذا', 'كيف ينتقل', 'انتقال']):
        section = "🦠 الأسباب:"
        next_sections = ["🔍 الأعراض:", "💊 العلاج:", "🛡️ الوقاية:", "📌 ملاحظة:"]
    elif any(word in question_lower for word in ['أعراض', 'علامات', 'يشخص', 'يظهر', 'مظهر']):
        section = "🔍 الأعراض:"
        next_sections = ["💊 العلاج:", "🛡️ الوقاية:", "📌 ملاحظة:"]
    elif any(word in question_lower for word in ['علاج', 'يعالج', 'دواء', 'كيف نعالج', 'معالجة']):
        section = "💊 العلاج:"
        next_sections = ["🛡️ الوقاية:", "📌 ملاحظة:"]
    elif any(word in question_lower for word in ['وقاية', 'نظافة', 'تجنب', 'حماية', 'منع']):
        section = "🛡️ الوقاية:"
        next_sections = ["📌 ملاحظة:"]
    else:
        return text
    
    start_idx = text.find(section)
    if start_idx == -1:
        return text
    
    end_idx = len(text)
    for next_section in next_sections:
        next_idx = text.find(next_section, start_idx + len(section))
        if next_idx != -1:
            end_idx = min(end_idx, next_idx)
    
    section_content = text[start_idx:end_idx].strip()
    if len(section_content) < 50:
        return section_content
    return section_content


def _format_fallback_response(context_chunks: list[dict] | None, question: str | None = None) -> str:
    snippets = []
    if context_chunks:
        for chunk in context_chunks[:3]:
            text = (chunk.get("text") or "").strip()
            if text:
                snippets.append(text[:500])
    combined = "\n\n".join(snippets)
    if combined:
        prefix = "الذكاء الاصطناعي غير متاح مؤقتاً. إليك المعلومات الأكثر صلة من قاعدة المعرفة"
        if question:
            prefix += f" لسؤالك: {question}"
        prefix += ":\n\n"
        return prefix + combined
    return "الذكاء الاصطناعي غير متاح مؤقتاً ولا توجد معلومات ذات صلة في قاعدة المعرفة."


class ConversationMemory:
    """Simple in-memory conversation history store."""
    def __init__(self):
        self._history: dict[str, list[dict]] = {}
        self._max_turns = 10

    def get_history(self, session_id: str) -> list[dict]:
        return self._history.get(session_id, [])

    def add_turn(self, session_id: str, question: str, answer: str) -> None:
        if session_id not in self._history:
            self._history[session_id] = []
        self._history[session_id].append({
            "question": question,
            "answer": answer,
        })
        if len(self._history[session_id]) > self._max_turns:
            self._history[session_id] = self._history[session_id][-self._max_turns:]

    def clear(self, session_id: str) -> None:
        self._history.pop(session_id, None)


conversation_memory = ConversationMemory()


class RAGPipeline:
    def __init__(self, retriever: Retriever | None = None, reranker: Reranker | None = None):
        self.retriever = retriever or Retriever()
        self.reranker = reranker or Reranker()
        self._llm_client = None
        self._init_llm_client()
        self._query_cache: dict[str, tuple[list[dict], ...]] = {}

    def _init_llm_client(self) -> None:
        if not settings.openrouter_api_key:
            return
        try:
            from openai import OpenAI  # noqa: PLC0415
        except ImportError:
            logger.warning("OpenAI SDK is not installed; falling back to local response mode.")
            return

        self._llm_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
        )

    def _get_cached_or_compute(self, query: str) -> list[dict]:
        """Return cached retrieval/rerank results if available, otherwise compute and cache."""
        cache_key = query.strip().lower()
        if cache_key in self._query_cache:
            return list(self._query_cache[cache_key])
        candidates = self.retriever.retrieve(query)
        top_chunks = self.reranker.rerank(query, candidates)
        self._query_cache[cache_key] = tuple(top_chunks)
        return top_chunks

    def answer_question(self, question: str, session_id: str = "default") -> dict:
        """Execute the full QA flow for a user-submitted question with conversation memory."""
        history = conversation_memory.get_history(session_id)
        top_chunks = self._get_cached_or_compute(question)
        
        messages = build_qa_prompt(question, top_chunks, history)
        response = self._call_llm(messages, context_chunks=top_chunks, question=question)
        
        response = _extract_relevant_section(response, question)
        
        conversation_memory.add_turn(session_id, question, response)
        
        return {"answer": response, "sources": top_chunks}

    def explain_diagnosis(self, disease_name: str, confidence: float) -> dict:
        """Explain a predicted disease using retrieved disease context."""
        candidates = self.retriever.retrieve_for_disease(disease_name)
        top_chunks = self.reranker.rerank(disease_name, candidates)
        messages = build_diagnosis_prompt(disease_name, confidence, top_chunks)
        response = self._call_llm(messages, context_chunks=top_chunks, question=disease_name)
        return {
            "disease": disease_name,
            "confidence": confidence,
            "explanation": response,
            "sources": top_chunks,
        }

    def _call_llm(self, messages: list[dict], context_chunks: list[dict] | None = None, question: str | None = None) -> str:
        """Call OpenRouter when configured; otherwise produce a useful fallback from the retrieved context."""
        if not self._llm_client:
            return _format_fallback_response(context_chunks, question)

        last_error = None
        for attempt in range(MAX_RETRIES):
            try:
                completion = self._llm_client.chat.completions.create(
                    model=settings.openrouter_model,
                    messages=messages,
                )
                return completion.choices[0].message.content or "No response generated."
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                is_transient = _is_transient_error(exc)
                should_retry = is_transient and attempt < MAX_RETRIES - 1
                if should_retry:
                    wait = RETRY_BACKOFF_BASE * (2 ** attempt)
                    logger.warning(
                        "OpenRouter transient error on attempt %d/%d: %s. Retrying in %.1fs...",
                        attempt + 1,
                        MAX_RETRIES,
                        exc,
                        wait,
                    )
                    time.sleep(wait)
                else:
                    logger.warning("Falling back because the LLM call failed: %s", exc)
                    break

        return _format_fallback_response(context_chunks, question)


def extract_diagnosis_fields(text: str) -> dict:
    """Parse the structured diagnosis text into fields."""
    result = {
        "disease": "",
        "confidence": "",
        "causes": "",
        "symptoms": "",
        "treatment": "",
        "prevention": "",
    }

    lines = text.split("\n")
    current_section = None
    section_content = []

    section_map = {
        "🦠 الأسباب:": "causes",
        "🔍 الأعراض:": "symptoms",
        "💊 العلاج:": "treatment",
        "🛡️ الوقاية:": "prevention",
    }

    for line in lines:
        line = line.strip()
        if not line:
            continue

        for emoji_header, field in section_map.items():
            if line.startswith(emoji_header):
                if current_section and section_content:
                    result[current_section] = "\n".join(section_content).strip()
                current_section = field
                section_content = []
                content = line[len(emoji_header):].strip()
                if content:
                    section_content.append(content)
                break
        else:
            if current_section:
                section_content.append(line)

    if current_section and section_content:
        result[current_section] = "\n".join(section_content).strip()

    return result
