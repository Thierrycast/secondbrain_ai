# schemas.py

from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    pergunta: str
    modelo: Optional[str] = None
    temperature: Optional[float] = None

class FormatRequest(BaseModel):
    path: str  # relativo ao VAULT_PATH
    force: bool = False  # permite reformatar notas já marcadas como formatadas
