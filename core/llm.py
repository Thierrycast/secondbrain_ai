import requests
import json
from config.config import OLLAMA_ENDPOINT, OLLAMA_MODEL, PROMPTS

DEBUG = True

def montar_prompt(tipo: str, conteudo: str, pergunta: str = "") -> str:
    template = PROMPTS.get(tipo, PROMPTS.get("pergunta"))
    return template.format(conteudo=conteudo, pergunta=pergunta)

def perguntar_ao_llm(tipo: str, conteudo: str, pergunta: str = "") -> str:
    full_prompt = montar_prompt(tipo, conteudo, pergunta)

    if DEBUG:
        print("\n[LLM] Enviando prompt:")
        print(full_prompt[:500], "...\n" if len(full_prompt) > 500 else "\n")

    try:
        response = requests.post(
            OLLAMA_ENDPOINT,
            json={"model": OLLAMA_MODEL, "prompt": full_prompt, "stream": False},
            timeout=180
        )
    except Exception as e:
        if DEBUG:
            print("[LLM] Erro ao conectar com Ollama:", str(e))
        return "[Erro ao conectar com o modelo]"

    if DEBUG:
        print("[LLM] RESPOSTA BRUTA DO MODELO:")
        print(response.text)

    try:
        data = response.json()
        resposta = data.get("response", "")
        if not isinstance(resposta, str):
            resposta = str(resposta)
    except Exception as e:
        if DEBUG:
            print("[LLM] Erro ao processar resposta JSON:", str(e))
        return "[Erro ao interpretar a resposta do modelo]"

    if not resposta:
        if DEBUG:
            print("[LLM] Nenhuma resposta recebida.")
        return "[Erro ao gerar resposta]"

    if DEBUG:
        print("[LLM] Resposta final (resumo):", resposta[:200])

    return resposta.strip()
