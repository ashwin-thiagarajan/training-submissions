from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    error_code: str
    message: str
    details: dict[str, Any] | None = None
    retryable: bool = False


class ValidationDetail(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field: str = Field(..., min_length=1)
    reason: str = Field(..., min_length=1)

