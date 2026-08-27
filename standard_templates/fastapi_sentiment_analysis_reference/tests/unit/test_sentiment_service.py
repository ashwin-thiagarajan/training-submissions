import pytest

from app.core.exceptions import InferenceFailedError, ModelNotReadyError
from app.core.config import Settings
from app.services.sentiment_service import SentimentService
from app.schemas.sentiment import SentimentRequest


def test_analyze_sentiment_returns_normalized_payload(test_settings: Settings) -> None:
    service = SentimentService(
        test_settings,
        pipeline_factory=lambda *_args, **_kwargs: lambda _text: [
            {"label": "POSITIVE", "score": 0.91}
        ],
    )
    service.load_model()

    response = service.analyze_sentiment(SentimentRequest(text="Great experience"))

    assert response.label == "positive"
    assert response.confidence == pytest.approx(0.91)
    assert response.input_size == len("Great experience")


def test_analyze_sentiment_requires_loaded_model(test_settings: Settings) -> None:
    service = SentimentService(test_settings, pipeline_factory=lambda *_args, **_kwargs: None)

    with pytest.raises(ModelNotReadyError):
        service.analyze_sentiment(SentimentRequest(text="hello"))


def test_analyze_sentiment_raises_for_unknown_label(test_settings: Settings) -> None:
    service = SentimentService(
        test_settings,
        pipeline_factory=lambda *_args, **_kwargs: lambda _text: [
            {"label": "MYSTERY", "score": 0.2}
        ],
    )
    service.load_model()

    with pytest.raises(InferenceFailedError):
        service.analyze_sentiment(SentimentRequest(text="hello"))


def test_readiness_reflects_service_state(test_settings: Settings) -> None:
    service = SentimentService(
        test_settings,
        pipeline_factory=lambda *_args, **_kwargs: lambda _text: [
            {"label": "NEGATIVE", "score": 0.77}
        ],
    )

    not_ready = service.readiness()
    assert not_ready.status == "not_ready"
    assert not not_ready.model_loaded

    service.load_model()
    ready = service.readiness()
    assert ready.status == "ready"
    assert ready.model_loaded

