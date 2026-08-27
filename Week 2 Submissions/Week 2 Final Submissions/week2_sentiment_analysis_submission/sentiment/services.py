from functools import lru_cache
from typing import Any

from django.conf import settings

from .exceptions import ModelInferenceError
from .schemas import SentimentRequest, SentimentResponse


class SentimentService:
    def __init__(self, pipeline_factory: Any | None = None) -> None:
        self.pipeline_factory = pipeline_factory
        self._pipeline = None

    def load_model(self) -> None:
        if self._pipeline is not None:
            return
        factory = self.pipeline_factory
        if factory is None:
            from transformers import pipeline

            factory = pipeline
        self._pipeline = factory(
            settings.SENTIMENT_MODEL_TASK,
            model=settings.SENTIMENT_MODEL_NAME,
        )

    def analyze(self, payload: SentimentRequest) -> SentimentResponse:
        try:
            self.load_model()
            raw_result = self._pipeline(payload.text)
        except Exception as exc:
            raise ModelInferenceError("Model inference failed.") from exc

        candidate = raw_result[0] if isinstance(raw_result, list) else raw_result
        label = str(candidate.get("label", "Neutral"))
        score = float(candidate.get("score", 0.0))
        return SentimentResponse(text=payload.text, sentiment=label, score=score)


@lru_cache
def get_sentiment_service() -> SentimentService:
    return SentimentService()