"""
Small shared utility functions used across the app.
Keep this module dependency-light — anything domain-specific belongs in
rag/ or vision/ instead.
"""

import hashlib
import time
from pathlib import Path


def file_hash(path: str | Path, chunk_size: int = 8192) -> str:
    """
    Compute a stable SHA-256 hash of a file's contents.
    Useful for de-duplicating PDFs before re-indexing them into ChromaDB.
    """
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def ensure_dir(path: str | Path) -> Path:
    """Create a directory (and parents) if it doesn't exist, return it as a Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


class Timer:
    """
    Small context manager for timing a block of code.

    Usage:
        with Timer() as t:
            do_something()
        print(t.elapsed_seconds)
    """

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        self.elapsed_seconds: float = 0.0
        return self

    def __exit__(self, *exc_info) -> None:
        self.elapsed_seconds = time.perf_counter() - self._start


# TODO: add validators for uploaded image files (size/type checks) here
# once app/api/upload.py is implemented.


class Translator:
    """Simple English-to-Arabic translator using deep-translator."""

    def __init__(self) -> None:
        self._translator = None

    def _get_translator(self):
        if self._translator is None:
            try:
                from deep_translator import GoogleTranslator
                self._translator = GoogleTranslator(source="en", target="ar")
            except Exception as exc:
                raise RuntimeError(f"Translation unavailable: {exc}") from exc
        return self._translator

    def translate(self, text: str) -> str:
        if not text or not text.strip():
            return text
        translator = self._get_translator()
        try:
            return translator.translate(text)
        except Exception:
            return text


translator = Translator()
