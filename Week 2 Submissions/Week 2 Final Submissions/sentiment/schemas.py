from pydantic import BaseModel, ConfigDict, Field, StrictStr


class SentimentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: StrictStr = Field(min_length=2, max_length=5000)


class SentimentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str
    sentiment: str
    score: float = Field(ge=0.0, le=1.0)

