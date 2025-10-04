# src/utils.py
import math
from typing import List

def chunk_text(text: str, max_words: int = 120, overlap_words: int = 20) -> List[str]:
    """
    Simple word-based chunker with overlap.
    Returns list of chunks (strings).
    """
    words = text.split()
    if len(words) <= max_words:
        return [text]
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+max_words]
        chunks.append(' '.join(chunk))
        i += max_words - overlap_words
        if i < 0:
            i = 0
    return chunks

def cosine_similarity(a, b):
    """
    expects numpy 1D arrays. returns cosine similarity scalar.
    """
    import numpy as np
    a = np.asarray(a)
    b = np.asarray(b)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)
