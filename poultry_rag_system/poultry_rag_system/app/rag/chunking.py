"""Split cleaned document text into overlapping chunks suitable for embedding."""

import re
from dataclasses import dataclass

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Chunk:
    text: str
    metadata: dict  # e.g. {"source": "newcastle_disease.pdf", "page": 3, "chunk_index": 2}


def _build_chunk(text: str, metadata: dict, chunk_index: int) -> Chunk:
    chunk_metadata = dict(metadata)
    source = chunk_metadata.get("source", "document")
    page = chunk_metadata.get("page", 1)
    chunk_metadata.update(
        {
            "page": page,
            "chunk_index": chunk_index,
            "chunk_id": f"{source}-{page}-{chunk_index}",
        }
    )
    return Chunk(text=text, metadata=chunk_metadata)


def chunk_text(
    text: str,
    metadata: dict,
    chunk_size: int = settings.chunk_size,
    chunk_overlap: int = settings.chunk_overlap,
) -> list[Chunk]:
    """Split text into overlapping text chunks while keeping metadata."""
    if not text.strip():
        return []

    cleaned_text = re.sub(r"\s+", " ", text).strip()
    if not cleaned_text:
        return []

    sentences = re.split(r"(?<=[.?!])\s+", cleaned_text)
    if len(sentences) > 1:
        chunks: list[Chunk] = []
        current: list[str] = []
        current_len = 0
        for sentence in sentences:
            sentence_words = len(re.findall(r"\S+", sentence))
            if current and current_len + sentence_words > max(12, chunk_size // 8):
                chunk_text = " ".join(current)
                chunks.append(_build_chunk(chunk_text, metadata, len(chunks)))
                current = [sentence]
                current_len = sentence_words
            else:
                current.append(sentence)
                current_len += sentence_words
        if current:
            chunks.append(_build_chunk(" ".join(current), metadata, len(chunks)))
        return chunks

    words = re.findall(r"\S+", cleaned_text)
    if not words:
        return []

    target_words = max(12, chunk_size // 8)
    overlap_words = max(0, chunk_overlap // 8)
    chunks: list[Chunk] = []
    start = 0
    chunk_index = 0

    while start < len(words):
        end = min(len(words), start + target_words)
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)
        if not chunk_text.strip():
            break

        chunks.append(_build_chunk(chunk_text, metadata, chunk_index))

        if end >= len(words):
            break
        next_start = end - overlap_words
        start = max(start + 1, next_start)
        chunk_index += 1

    return chunks
