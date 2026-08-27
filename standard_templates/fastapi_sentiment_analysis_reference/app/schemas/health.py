from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReadinessResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str
    model_loaded: bool
    version: str
    checked_at: datetime

