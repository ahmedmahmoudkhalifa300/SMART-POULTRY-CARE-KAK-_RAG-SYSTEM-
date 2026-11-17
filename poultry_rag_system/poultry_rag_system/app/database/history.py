"""
Lightweight persistence for chat/diagnosis history, so the Streamlit UI can
show past conversations and diagnoses across sessions.

Not part of the core RAG/vision logic — kept isolated so the storage
backend can be swapped (SQLite now, Postgres later) without touching the
pipelines.
"""

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

from pathlib import Path

# Dynamically resolve DB_PATH to ensure it is in the project's root data folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = str(PROJECT_ROOT / "data" / "history.sqlite3")


@contextmanager
def get_connection():
    """
    Provide a transactional scope around database operations.
    Automatically commits on success or rolls back on exception.
    """
    db_file = Path(DB_PATH)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """
    Create tables if they don't exist yet.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS diagnosis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease TEXT NOT NULL,
                confidence REAL NOT NULL,
                explanation TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )


def log_chat(question: str, answer: str) -> None:
    """Insert a chat Q&A turn into the database."""
    created_at = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (question, answer, created_at) VALUES (?, ?, ?)",
            (question, answer, created_at),
        )


def log_diagnosis(disease: str, confidence: float, explanation: str) -> None:
    """Insert a disease diagnosis record into the database."""
    created_at = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO diagnosis_history (disease, confidence, explanation, created_at) VALUES (?, ?, ?, ?)",
            (disease, confidence, explanation, created_at),
        )
