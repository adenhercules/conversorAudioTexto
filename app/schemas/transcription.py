from pydantic import BaseModel, ConfigDict

class TranscriptionResponse(BaseModel):
    filename: str
    content_type: str
    transcription: str
    language: str

    model_config = ConfigDict(from_attributes=True)
