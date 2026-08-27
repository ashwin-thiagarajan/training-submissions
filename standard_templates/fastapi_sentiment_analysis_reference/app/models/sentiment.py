from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class ServiceState:
    model_name: str
    max_input_chars: int
    model_pipeline: Any | None = None
    startup_completed: bool = False
    last_model_load_error: str | None = None


@dataclass(slots=True)
class SentimentInference:
    request_id: str
    label: str
    confidence: float
    model_name: str
    input_size: int
    processed_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

