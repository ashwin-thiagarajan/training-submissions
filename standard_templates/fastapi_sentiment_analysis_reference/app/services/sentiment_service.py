from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone
from typing import Any

from app.core.config import Settings
from app.core.exceptions import InferenceFailedError, ModelNotReadyError
from app.core.logging import get_logger
from app.models.sentiment import SentimentInference, ServiceState
from app.schemas.health import ReadinessResponse
from app.schemas.sentiment import SentimentRequest, SentimentResponse
from app.utils.text_normalization import normalize_text


class SentimentService:
    def __init__(
        self,
        settings: Settings,
        pipeline_factory: Any | None = None,
    ) -> None:
        self.settings = settings
        self.pipeline_factory = pipeline_factory
        self.state = ServiceState(
            model_name=settings.model_name,
            max_input_chars=settings.max_input_chars,
        )
        self.logger = get_logger("service.sentiment_service")

    def load_model(self) -> None:
        if self.state.model_pipeline is not None:
            return

        started = time.perf_counter()
        try:
            factory = self.pipeline_factory
            if factory is None:
                from transformers import pipeline

                factory = pipeline
            self.state.model_pipeline = factory(
                self.settings.model_task,
                model=self.settings.model_name,
            )
            self.state.startup_completed = True
            self.state.last_model_load_error = None
        except Exception as exc:  # pragma: no cover - exercised via tests with mocks
            self.state.model_pipeline = None
            self.state.startup_completed = False
            self.state.last_model_load_error = str(exc)
            raise ModelNotReadyError() from exc
        finally:
            duration_ms = round((time.perf_counter() - started) * 1000, 2)
            self.logger.info(
                "model_load_completed",
                extra={
                    "operation": "model_load",
                    "duration_ms": duration_ms,
                    "model_name": self.settings.model_name,
                    "loaded": self.state.model_pipeline is not None,
                },
            )

    def readiness(self) -> ReadinessResponse:
        ready = self.state.model_pipeline is not None and self.state.startup_completed
        return ReadinessResponse(
            status="ready" if ready else "not_ready",
            model_loaded=ready,
            version=self.settings.app_version,
            checked_at=datetime.now(timezone.utc),
        )

    def analyze_sentiment(
        self,
        payload: SentimentRequest,
        request_id: str | None = None,
    ) -> SentimentResponse:
        if self.state.model_pipeline is None:
            raise ModelNotReadyError()

        normalized = normalize_text(payload.text, self.settings.max_input_chars)
        correlation_id = payload.request_id or request_id or str(uuid.uuid4())

        preprocess_started = time.perf_counter()
        # Normalization already completed above; log the preprocessing interval.
        preprocess_duration = round((time.perf_counter() - preprocess_started) * 1000, 2)
        self.logger.info(
            "preprocess_completed",
            extra={
                "operation": "preprocess",
                "duration_ms": preprocess_duration,
                "request_id": correlation_id,
                "input_size": normalized.input_size,
            },
        )

        infer_started = time.perf_counter()
        try:
            raw_result = self.state.model_pipeline(normalized.text)
        except Exception as exc:
            raise InferenceFailedError() from exc
        infer_duration = round((time.perf_counter() - infer_started) * 1000, 2)
        self.logger.info(
            "model_inference_completed",
            extra={
                "operation": "model_inference",
                "duration_ms": infer_duration,
                "request_id": correlation_id,
                "input_size": normalized.input_size,
            },
        )

        result = self._normalize_result(raw_result, correlation_id, normalized.input_size)
        return SentimentResponse(
            request_id=result.request_id,
            label=result.label,
            confidence=result.confidence,
            model_name=result.model_name,
            input_size=result.input_size,
            processed_at=result.processed_at,
        )

    def _normalize_result(
        self,
        raw_result: Any,
        request_id: str,
        input_size: int,
    ) -> SentimentInference:
        if isinstance(raw_result, list):
            candidate = raw_result[0] if raw_result else None
        else:
            candidate = raw_result
        if not isinstance(candidate, dict):
            raise InferenceFailedError("Sentiment inference returned an unexpected payload.")

        raw_label = str(candidate.get("label", "")).lower()
        raw_score = float(candidate.get("score", 0.0))
        label = self._map_label(raw_label)
        if label is None:
            raise InferenceFailedError("Sentiment inference returned an unsupported label.")

        return SentimentInference(
            request_id=request_id,
            label=label,
            confidence=raw_score,
            model_name=self.settings.model_name,
            input_size=input_size,
        )

    @staticmethod
    def _map_label(raw_label: str) -> str | None:
        if "positive" in raw_label or raw_label.endswith("pos"):
            return "positive"
        if "negative" in raw_label or raw_label.endswith("neg"):
            return "negative"
        if "neutral" in raw_label or raw_label.endswith("neu"):
            return "neutral"
        return None

