from fastapi import FastAPI

from src.interfaces.api.routes.transcription import router as transcription_router
from src.interfaces.api.routes.prosody import router as prosody_router


app = FastAPI(title="Treinador de Vendas com IA - API", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Rotas
app.include_router(transcription_router, prefix="/transcriptions", tags=["transcriptions"])
app.include_router(prosody_router, prefix="/prosody", tags=["prosody"])
