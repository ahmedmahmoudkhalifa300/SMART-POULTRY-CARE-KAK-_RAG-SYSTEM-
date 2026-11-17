"""
Loads the trained poultry disease image classifier and exposes a simple
predict() interface. Keeping model loading isolated here means it only
happens once (lazy singleton) rather than per-request.
"""

import numpy as np

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

_model = None


class PoultryClassifier:
    def __init__(self, model_path: str = settings.model_path):
        self.model_path = model_path
        self.class_names = settings.disease_classes

    def _load(self):
        global _model
        if _model is None:
            import tensorflow as tf
            logger.info(f"Loading classifier from {self.model_path}")
            _model = tf.keras.models.load_model(self.model_path)
            logger.info(f"Loaded {len(self.class_names)} classes: {self.class_names}")
        return _model

    def predict_proba(self, preprocessed_image: np.ndarray) -> np.ndarray:
        """Run inference and return raw class probabilities."""
        model = self._load()
        return model.predict(preprocessed_image, verbose=0)[0]


def get_classifier() -> PoultryClassifier:
    return PoultryClassifier()
