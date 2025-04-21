from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.state import get_store
from core.formatter import formatar_nota_em_arquivo
from core.llm_utils import responder_pergunta
from server.schemas import QueryRequest, FormatRequest
import uvicorn

DATA_PATH = "data"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = get_store()

@app.post("/query")
async def query(req: QueryRequest):
    print(f"[API] Recebida pergunta: {req.pergunta}")
    resposta = responder_pergunta(
        pergunta=req.pergunta,
        store=store
    )
    print(f"[API] Resposta gerada com {len(resposta)} caracteres")
    return {"resposta": resposta}

@app.post("/formatar-nota")
async def formatar_nota(req: FormatRequest):
    print(f"[API] Solicitada formatação: {req.path} (force={req.force})")
    resultado = formatar_nota_em_arquivo(req.path, force=req.force)
    print(f"[API] Resultado: {resultado}")
    return resultado

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=11435, reload=True)
