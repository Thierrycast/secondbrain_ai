# atualizar_index.py

from core.parser import carregar_notas_pasta
from core.embedder import gerar_embeddings
from core.vector_store import VetorStore
from config.config import VAULT_PATH
from utils.index_metadata import carregar_metadados, salvar_metadados, listar_md_com_hash

import os
import numpy as np

DATA_PATH = "data"

print("Verificando mudanças no vault...")

metadados_antigos = carregar_metadados()
hashes_atualizados = listar_md_com_hash(VAULT_PATH)

novos_ou_modificados = [arquivo for arquivo, hash_ in hashes_atualizados.items()
                        if arquivo not in metadados_antigos or metadados_antigos[arquivo] != hash_]

if not novos_ou_modificados:
    print("Nada novo ou alterado. Índice já está atualizado.")
    exit()

print(f"{len(novos_ou_modificados)} arquivos novos ou modificados detectados.")

# Carrega índice salvo
store = VetorStore.carregar_de_arquivo(DATA_PATH)
if not store:
    print("Nenhum índice existente. Criando novo...")
    store = None

notas = carregar_notas_pasta(VAULT_PATH)
notas_dict = {nota["caminho"]: nota for nota in notas}

novos_textos = [notas_dict[c]["conteudo"] for c in novos_ou_modificados if c in notas_dict]

if not novos_textos:
    print("Nenhuma nota correspondente encontrada para embeddar.")
    exit()

print("Gerando embeddings para novos conteúdos...")
novos_embeddings = gerar_embeddings(novos_textos)

if store is None:
    store = VetorStore(dimensao=novos_embeddings.shape[1])

store.adicionar(novos_embeddings, novos_textos)
store.salvar_em_arquivo(DATA_PATH)
salvar_metadados(hashes_atualizados)

print("Atualização do índice concluída com sucesso!")
