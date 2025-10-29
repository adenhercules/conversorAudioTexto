import whisper
import tempfile
import os
from fastapi import UploadFile
from app.schemas.transcription import TranscriptionResponse

print("Carregando o modelo Whisper 'base'...")
try:
    model = whisper.load_model("base")
    print("Modelo 'base' carregado com sucesso.")
except Exception as e:
    print(f"Erro ao carregar o modelo Whisper: {e}")
    raise e


# -----------------------------------------------------------------------------
# Função de Transcrição
# -----------------------------------------------------------------------------

def transcribe_audio(file: UploadFile) -> TranscriptionResponse:
    """
    Recebe um objeto UploadFile do FastAPI, salva-o temporariamente
    e usa o Whisper para transcrever o áudio.

    Retorna um objeto TranscriptionResponse em caso de sucesso.
    Levanta uma Exceção em caso de falha.
    """
    temp_file_path = None
    try:
        file_extension = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(file.file.read())
            temp_file_path = temp_file.name

        print(f"Arquivo temporário salvo em: {temp_file_path}")

        result = model.transcribe(temp_file_path, fp16=False)

        print("Transcrição concluída.")

        return TranscriptionResponse(
            filename=file.filename,
            content_type=file.content_type,
            transcription=result.get("text", ""),
            language=result.get("language", "")
        )

    except Exception as e:
        print(f"Erro durante a transcrição: {e}")
        raise e

    finally:

        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"Arquivo temporário {temp_file_path} deletado.")

