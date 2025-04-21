from dotenv import load_dotenv
import os
import json

load_dotenv()

# Caminho da pasta contendo as notas do Obsidian
VAULT_PATH = "vault"

OLLAMA_MODEL = os.environ["OLLAMA_MODEL"]
OLLAMA_ENDPOINT = os.environ["OLLAMA_ENDPOINT"]
LISTEN_INTERVAL = int(os.environ.get("LISTEN_INTERVAL", 10))

# Caminhos de prompts
PROMPT_PATH = os.environ.get("PROMPT_PATH", "prompts/pessoal.json")

try:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        PROMPTS = json.load(f)
except FileNotFoundError:
    with open("prompts/default.json", "r", encoding="utf-8") as f:
        PROMPTS = json.load(f)
