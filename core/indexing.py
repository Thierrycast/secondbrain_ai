from core.parser import carregar_notas_pasta
from core.embedder import gerar_embeddings
from core.vector_store import VetorStore
from utils.index_metadata import carregar_metadados, salvar_metadados, listar_md_com_hash
from config.config import VAULT_PATH, LISTEN_INTERVAL

import os
import time

DATA_PATH = "data"

def construir_texto_completo(nota: dict) -> str:
    partes = []
    if nota.get("hierarquia"):
        partes.append(f"Hierarquia: {nota['hierarquia']}")
    partes.append(f"Título: {nota['titulo']}")
    if nota.get("tags"):
        partes.append(f"Tags: {', '.join(nota['tags'])}")
    partes.append("\n" + nota["conteudo"].strip())
    return "\n".join(partes)

def reindexar():
    print("Reindexando completamente o índice...")
    notas = carregar_notas_pasta(VAULT_PATH)
    textos = [construir_texto_completo(n) for n in notas]

    embeddings = gerar_embeddings(textos)
    store = VetorStore(dimensao=embeddings.shape[1])
    store.adicionar(embeddings, textos)
    store.salvar_em_arquivo(DATA_PATH)

    hashes = listar_md_com_hash(VAULT_PATH)
    salvar_metadados(hashes)

    print("Reindexação concluída.")
    return store

def atualizar_index_se_necessario(store):
    print("Verificando atualizações no vault...")
    metadados_antigos = carregar_metadados()
    hashes_atualizados = listar_md_com_hash(VAULT_PATH)

    novos_ou_modificados = [arquivo for arquivo, hash_ in hashes_atualizados.items()
                            if arquivo not in metadados_antigos or metadados_antigos[arquivo] != hash_]

    if not novos_ou_modificados:
        print("Nenhuma atualização detectada.")
        return store

    print(f"Detectados {len(novos_ou_modificados)} arquivos novos ou modificados.")

    if store is None:
        store = VetorStore.carregar_de_arquivo(DATA_PATH)

    if not store:
        print("Nenhum índice existente. Criando novo...")

    notas = carregar_notas_pasta(VAULT_PATH)
    notas_dict = {nota["caminho"]: nota for nota in notas}
    novos_textos = [construir_texto_completo(notas_dict[c]) for c in novos_ou_modificados if c in notas_dict]

    if not novos_textos:
        print("Nenhuma nota correspondente encontrada para embeddar.")
        return store

    print("Gerando embeddings para os novos conteúdos...")
    novos_embeddings = gerar_embeddings(novos_textos)

    if store is None:
        store = VetorStore(dimensao=novos_embeddings.shape[1])

    store.adicionar(novos_embeddings, novos_textos)
    store.salvar_em_arquivo(DATA_PATH)
    salvar_metadados(hashes_atualizados)

    print("Índice atualizado com sucesso!")
    return store

def iniciar_listen_loop():
    print(f"🔄 Iniciando modo de escuta por alterações no vault a cada {LISTEN_INTERVAL} segundos...")
    store = VetorStore.carregar_de_arquivo(DATA_PATH)
    if not store:
        print("Nenhum índice encontrado. Reindexando...")
        store = reindexar()

    try:
        while True:
            store = atualizar_index_se_necessario(store)
            time.sleep(LISTEN_INTERVAL)
    except KeyboardInterrupt:
        print("⏹️ Encerrado o modo de escuta.")