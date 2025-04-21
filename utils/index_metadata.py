# utils/index_metadata.py

import os
import hashlib
import json
from typing import Dict

ARQUIVO_METADADOS = os.path.join("data", "index_metadata.json")

def gerar_hash_arquivo(caminho: str) -> str:
    """Gera um hash SHA-256 eficiente lendo o arquivo em blocos."""
    hasher = hashlib.sha256()
    try:
        with open(caminho, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
    except Exception as e:
        print(f"⚠️ Erro ao calcular hash de {caminho}: {e}")
        return ""
    return hasher.hexdigest()

def listar_md_com_hash(pasta: str) -> Dict[str, str]:
    """Percorre recursivamente uma pasta listando arquivos .md e seus hashes."""
    arquivos_hash = {}
    for raiz, _, arquivos in os.walk(pasta):
        for nome in arquivos:
            if nome.endswith(".md") and not nome.startswith("."):
                caminho = os.path.join(raiz, nome)
                hash_arquivo = gerar_hash_arquivo(caminho)
                if hash_arquivo:
                    arquivos_hash[caminho] = hash_arquivo
    return arquivos_hash

def carregar_metadados() -> Dict[str, str]:
    """Carrega o arquivo de metadados de hash, ou retorna vazio se não existir."""
    if not os.path.exists(ARQUIVO_METADADOS):
        return {}
    with open(ARQUIVO_METADADOS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_metadados(hashes: Dict[str, str]) -> None:
    """Salva os metadados de hash no arquivo JSON."""
    with open(ARQUIVO_METADADOS, "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2, ensure_ascii=False)