import os
import sqlite3
import unittest
from pathlib import Path

# Override DB_PATH to a temporary location for testing
import app.database.history
TEST_DB_PATH = "./data/test_history.sqlite3"
app.database.history.DB_PATH = TEST_DB_PATH

from app.database.history import init_db, log_chat, log_diagnosis, get_connection


class DatabaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure test database does not exist initially
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def setUp(self):
        init_db()

    def tearDown(self):
        if os.path.exists(TEST_DB_PATH):
            try:
                os.remove(TEST_DB_PATH)
            except PermissionError:
                pass

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEST_DB_PATH):
            try:
                os.remove(TEST_DB_PATH)
            except PermissionError:
                pass

    def test_init_db_creates_tables(self) -> None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            self.assertIn("chat_history", tables)
            self.assertIn("diagnosis_history", tables)

    def test_log_chat_inserts_record(self) -> None:
        log_chat("How is Newcastle disease transmitted?", "It is highly contagious and spreads via aerosol and secretions.")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT question, answer, created_at FROM chat_history;")
            rows = cursor.fetchall()
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0][0], "How is Newcastle disease transmitted?")
            self.assertEqual(rows[0][1], "It is highly contagious and spreads via aerosol and secretions.")
            self.assertTrue(rows[0][2]) # check non-empty timestamp

    def test_log_diagnosis_inserts_record(self) -> None:
        log_diagnosis("Coccidiosis", 0.95, "Detailed explanation of symptoms and treatment.")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT disease, confidence, explanation, created_at FROM diagnosis_history;")
            rows = cursor.fetchall()
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0][0], "Coccidiosis")
            self.assertEqual(rows[0][1], 0.95)
            self.assertEqual(rows[0][2], "Detailed explanation of symptoms and treatment.")
            self.assertTrue(rows[0][3])


if __name__ == "__main__":
    unittest.main()
