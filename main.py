from fastapi import FastAPI

from app.api.documents import router as documents_router
from app.api.chat import router as chat_router


app = FastAPI(
    title="Maha-GR RAG API",
    description=(
        "Source-grounded question answering system "
        "for Government of Maharashtra documents."
    ),
    version="0.1.0",
)


app.include_router(
    documents_router
)

app.include_router(
    chat_router
)


@app.get("/")
def root():
    return {
        "name": "Maha-GR RAG API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }