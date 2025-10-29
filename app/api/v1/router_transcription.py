from fastapi import APIRouter, UploadFile, File, HTTPException
import mimetypes
from app.services.transcriber_service import transcribe_audio
from app.schemas.transcription import TranscriptionResponse
router = APIRouter()


@router.post("/transcrever-audio/", response_model=TranscriptionResponse)
async def api_transcrever_audio(audio_file: UploadFile = File(...)):
    """
    Recebe um arquivo de áudio e retorna a transcrição.
    ...
    """

    mime_type, _ = mimetypes.guess_type(audio_file.filename)

    if not mime_type or not mime_type.startswith("audio/"):
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de arquivo não suportado: {audio_file.filename}. Envie um arquivo de áudio (mp3, wav, m4a, etc.)."
        )

    print(f"Recebido arquivo: {audio_file.filename} (Tipo: {mime_type})")

    try:
        result = transcribe_audio(audio_file)

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro inesperado ao processar o arquivo: {str(e)}")
