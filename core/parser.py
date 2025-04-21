import os
import frontmatter
from typing import List, Dict

def carregar_notas_pasta(pasta: str) -> List[Dict]:
    notas = []
    for raiz, _, arquivos in os.walk(pasta):
        for nome_arquivo in arquivos:
            if not nome_arquivo.endswith(".md") or nome_arquivo.startswith("."):
                continue

            caminho = os.path.join(raiz, nome_arquivo)
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    hierarquia = os.path.relpath(raiz, pasta).replace(os.sep, " > ") if raiz != pasta else ""

                    notas.append({
                        "titulo": post.get("title") or nome_arquivo.replace(".md", ""),
                        "tags": post.get("tags", []),
                        "conteudo": post.content,
                        "caminho": caminho,
                        "hierarquia": hierarquia
                    })
            except Exception as e:
                print(f"⚠️ Erro ao carregar nota: {caminho} — {e}")
    return notas
