from core.indexing import atualizar_index_se_necessario
from core.vector_store import VetorStore
import os

DATA_PATH = "data"

_store = None

def get_store():
    global _store
    if _store is None:
        _store = atualizar_index_se_necessario(None)
        if not _store:
            _store = VetorStore.carregar_de_arquivo(DATA_PATH)
    return _store
