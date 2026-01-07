from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Any

_MODEL: Any = None

def _get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _MODEL

def get_embedding(text: str) -> np.ndarray:
    """
    Returns a 1-D numpy array embedding for the given text.
    """
    model = _get_model()
    vec = model.encode(text, show_progress_bar=False)
    return np.asarray(vec, dtype=float)
