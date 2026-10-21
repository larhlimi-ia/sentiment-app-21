from pydantic import BaseModel, field_validator


class PredictionRequest(BaseModel):
    text: str

    @field_validator('text')
    @classmethod
    def text_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('texte vide')
        if len(v) > 2000:
            raise ValueError('texte trop long (max 2000 caractères)')
        return v


class PredictionResponse(BaseModel):
    text: str
    label: str
    score: float