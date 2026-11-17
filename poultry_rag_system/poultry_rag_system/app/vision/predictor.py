"""
End-to-end prediction flow: raw uploaded image bytes -> preprocessing ->
classifier -> a clean, human-readable prediction result.
"""

import numpy as np
from dataclasses import dataclass

from app.core.logger import get_logger
from app.vision.classifier import PoultryClassifier, get_classifier
from app.vision.preprocessing import load_image, preprocess_image

logger = get_logger(__name__)


@dataclass
class DiagnosisPrediction:
    disease: str
    confidence: float
    all_probabilities: dict  # {class_name: probability}


class Predictor:
    def __init__(self, classifier: PoultryClassifier | None = None):
        self.classifier = classifier or get_classifier()

    def predict(self, file_bytes: bytes) -> DiagnosisPrediction:
        image = load_image(file_bytes)
        array = preprocess_image(image)
        probs = self.classifier.predict_proba(array)
        best_idx = int(np.argmax(probs))
        return DiagnosisPrediction(
            disease=self.classifier.class_names[best_idx],
            confidence=float(probs[best_idx]),
            all_probabilities=dict(zip(self.classifier.class_names, probs.tolist())),
        )
