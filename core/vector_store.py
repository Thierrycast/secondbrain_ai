import faiss
import numpy as np
import json
import os
from typing import List, Tuple

class VetorStore:
    def __init__(self, dimensao: int):
        self.index = faiss.IndexFlatIP(dimensao)
        self.textos: List[str] = []

    def adicionar(self, embeddings: np.ndarray, textos: List[str]):
        self.index.add(embeddings)
        self.textos.extend(textos)

    def buscar(self, consulta: np.ndarray, k: int = 5) -> List[Tuple[str, float]]:
        distancias, indices = self.index.search(consulta, k)
        resultados = []
        for i, idx in enumerate(indices[0]):
            texto = self.textos[idx]
            score = float(distancias[0][i])
            resultados.append((texto, score))
        return resultados

    def salvar_em_arquivo(self, pasta: str):
        os.makedirs(pasta, exist_ok=True)

        # Salva o índice FAISS
        faiss.write_index(self.index, os.path.join(pasta, "index.faiss"))

        # Salva os textos em JSON
        with open(os.path.join(pasta, "textos.json"), "w", encoding="utf-8") as f:
            json.dump(self.textos, f, ensure_ascii=False, indent=2)

    @staticmethod
    def carregar_de_arquivo(pasta: str):
        index_path = os.path.join(pasta, "index.faiss")
        textos_path = os.path.join(pasta, "textos.json")

        if not os.path.exists(index_path) or not os.path.exists(textos_path):
            return None

        index = faiss.read_index(index_path)
        with open(textos_path, "r", encoding="utf-8") as f:
            textos = json.load(f)

        store = VetorStore(dimensao=index.d)
        store.index = index
        store.textos = textos
        return store
