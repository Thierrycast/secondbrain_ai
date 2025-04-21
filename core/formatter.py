import os
import frontmatter
from core.llm import perguntar_ao_llm
from config.config import VAULT_PATH

def formatar_nota_em_arquivo(rel_path: str, force: bool = False) -> dict:
    full_path = os.path.join(VAULT_PATH, rel_path)
    print(f"[Formatter] Caminho completo: {full_path}")

    if not os.path.exists(full_path):
        print("[Formatter] Arquivo não encontrado.")
        return {"erro": "Arquivo não encontrado."}

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            nota = frontmatter.load(f)
        print("[Formatter] Nota carregada com sucesso.")
    except Exception as e:
        print("[Formatter] Erro ao carregar nota:", str(e))
        return {"erro": f"Erro ao carregar a nota: {str(e)}"}

    if nota.get("formated") is True and not force:
        print("[Formatter] Nota já formatada, e 'force' não foi definido.")
        return {"resposta": "Esta nota já está marcada como formatada. Use 'force' para sobrescrever."}

    try:
        print("[Formatter] Conteúdo da nota antes do envio:")
        print(nota.content[:300])
        resposta = perguntar_ao_llm("formatar", nota.content)
        nota.content = str(resposta).strip()
        nota["formated"] = True

        print("[Formatter] Salvando nota formatada...")
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(nota))
        print("[Formatter] Nota salva com sucesso.")

        return {"resposta": "Nota formatada com sucesso."}
    except Exception as e:
        print("[Formatter] Erro ao processar a nota:", str(e))
        return {"erro": f"Erro ao processar a nota: {str(e)}"}
