from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Any

_MODEL: Any = None

def _get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
    return _MODEL

def get_embedding(text: str) -> np.ndarray:
    model = _get_model()
    return np.asarray(
        model.encode(text, show_progress_bar=False),
        dtype=float
    )
