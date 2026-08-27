from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SentimentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., min_length=1)
    language_hint: str | None = Field(default=None, min_length=2, max_length=32)
    request_id: str | None = Field(default=None, min_length=1, max_length=128)

    @field_validator("text")
    @classmethod
    def validate_text_present(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Text must not be empty.")
        return value


class SentimentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    label: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    model_name: str
    input_size: int = Field(..., ge=1)
    processed_at: datetime

