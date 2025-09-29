from fastapi import FastAPI
import logging
import os

from src.interfaces.api.routes.transcription import router as transcription_router
from src.interfaces.api.routes.prosody import router as prosody_router
from src.interfaces.api.routes.transcription_read import router as transcription_read_router
from src.interfaces.api.routes.prosody_read import router as prosody_read_router
from src.infrastructure.db.sqlite import init_db


app = FastAPI(title="Treinador de Vendas com IA - API", version="0.1.0")

# Configuração de logging simples para dev
if os.getenv("DEMO_MODE", "false").lower() == "true":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')

# Inicializa o banco (cria tabelas se não existirem)
init_db()


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Rotas
app.include_router(transcription_router, prefix="/transcriptions", tags=["transcriptions"])
app.include_router(prosody_router, prefix="/prosody", tags=["prosody"])
app.include_router(transcription_read_router, prefix="/transcriptions", tags=["transcriptions-read"])
app.include_router(prosody_read_router, prefix="/prosody", tags=["prosody-read"])
