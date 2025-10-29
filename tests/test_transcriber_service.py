import pytest
from fastapi import UploadFile
from io import BytesIO
from app.services.transcriber_service import transcribe_audio, TranscriptionResponse


# Subclasse mockável com content_type configurável
class MockUploadFile(UploadFile):
    def __init__(self, filename, file, content_type="audio/mpeg"):
        super().__init__(filename=filename, file=file)
        self._content_type = content_type

    @property
    def content_type(self):
        return self._content_type


@pytest.fixture
def mock_upload_file():
    """Cria um arquivo de áudio falso para o teste"""
    audio_bytes = b"FAKE AUDIO DATA"
    return MockUploadFile(filename="teste.mp3", file=BytesIO(audio_bytes), content_type="audio/mpeg")


def test_transcribe_audio_success(mocker, mock_upload_file):
    """Teste de sucesso da transcrição"""
    mock_model = mocker.patch("app.services.transcriber_service.model")
    mock_model.transcribe.return_value = {
        "text": "Olá, mundo!",
        "language": "pt"
    }

    result = transcribe_audio(mock_upload_file)

    assert isinstance(result, TranscriptionResponse)
    assert result.transcription == "Olá mundo!"
    assert result.language == "pt"
    assert result.filename == "teste.mp3"
    assert result.content_type == "audio/mpeg"


def test_transcribe_audio_failure(mocker, mock_upload_file):
    """Teste de erro durante a transcrição"""
    mock_model = mocker.patch("app.services.transcriber_service.model")
    mock_model.transcribe.side_effect = Exception("Erro no modelo Whisper")

    with pytest.raises(Exception) as exc_info:
        transcribe_audio(mock_upload_file)

    assert "Erro no modelo Whisper" in str(exc_info.value)
