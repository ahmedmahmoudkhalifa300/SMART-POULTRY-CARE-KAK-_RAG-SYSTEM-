"""
Prepares uploaded poultry images for the classifier: resizing, normalization,
and basic validity checks.
"""

import io

import numpy as np
from PIL import Image

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


def load_image(file_bytes: bytes) -> Image.Image:
    """Load raw uploaded bytes into a PIL Image."""
    try:
        image = Image.open(io.BytesIO(file_bytes))
        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")
        elif image.mode == "L":
            image = image.convert("RGB")
        return image
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"Unable to load image: {exc}") from exc


def preprocess_image(image: Image.Image) -> np.ndarray:
    """Resize + normalize an image into the exact shape/scale the trained model expects."""
    image = image.resize(settings.image_size)
    array = np.asarray(image, dtype=np.float32) / 255.0
    array = np.expand_dims(array, axis=0)
    return array
