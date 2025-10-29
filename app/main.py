from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import router_transcription

app = FastAPI(
    title="API Conversora de Áudio para Texto",
    description="Uma API que usa OpenAI Whisper para transcrever arquivos de áudio.",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_transcription.router, prefix="/api/v1")