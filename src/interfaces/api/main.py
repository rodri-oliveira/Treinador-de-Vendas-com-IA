from fastapi import FastAPI

app = FastAPI(title="Treinador de Vendas com IA - API", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}
