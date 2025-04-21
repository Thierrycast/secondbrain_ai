from core.embedder import gerar_embeddings
from core.llm import perguntar_ao_llm


def responder_pergunta(pergunta: str, store) -> str:
    if not store:
        return "[Erro: índice não disponível]"

    consulta = gerar_embeddings([pergunta])
    resultados = store.buscar(consulta, k=3)
    contexto = "\n---\n".join([texto for texto, _ in resultados])
    return perguntar_ao_llm(contexto, pergunta)
