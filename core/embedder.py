
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

modelo = SentenceTransformer('all-MiniLM-L6-v2')

def gerar_embeddings(textos: List[str], batch_size: int = 32) -> np.ndarray:
    return modelo.encode(
        textos,
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )
