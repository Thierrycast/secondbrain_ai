from core.indexing import reindexar, iniciar_listen_loop, atualizar_index_se_necessario
from core.vector_store import VetorStore
from core.embedder import gerar_embeddings
from core.llm import perguntar_ao_llm

import sys
import os

DATA_PATH = "data"

def executar():
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

    if len(sys.argv) > 1:
        if sys.argv[1] == "--reindexar":
            reindexar()
            return
        elif sys.argv[1] == "--escutar":
            iniciar_listen_loop()
            return
        else:
            print("Comando não reconhecido. Use --reindexar ou --escutar")
            return

    store = atualizar_index_se_necessario(None)
    if not store:
        store = VetorStore.carregar_de_arquivo(DATA_PATH)

    if not store:
        print("Não foi possível carregar ou gerar o índice.")
        return

    print("Pronto! Digite sua pergunta ou 'sair' para encerrar.")

    while True:
        pergunta = input("\n> ")
        import time
        t0 = time.perf_counter()

        if pergunta.lower() == "sair":
            break

        t1 = time.perf_counter()
        consulta = gerar_embeddings([pergunta])
        t2 = time.perf_counter()

        resultados = store.buscar(consulta, k=3)
        t3 = time.perf_counter()

        contexto = "\n---\n".join([texto for texto, _ in resultados])
        t4 = time.perf_counter()

        resposta = perguntar_ao_llm(contexto, pergunta)
        t5 = time.perf_counter()

        print(f"\n⏱️ Desempenho: Embedding={t2 - t1:.2f}s | Busca={t3 - t2:.2f}s | Contexto={t4 - t3:.2f}s | LLM={t5 - t4:.2f}s | Total={t5 - t0:.2f}s")
