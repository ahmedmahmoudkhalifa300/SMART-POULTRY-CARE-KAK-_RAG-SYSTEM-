"""
Global state for the RAG pipeline warm-up.
"""

import threading

class AppState:
    def __init__(self):
        self.pipeline = None
        self.pipeline_ready = threading.Event()


state = AppState()