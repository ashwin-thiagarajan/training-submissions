from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app
from app.services.sentiment_service import SentimentService


def fake_pipeline(_text: str) -> list[dict[str, float | str]]:
    return [{"label": "positive", "score": 0.98}]


@pytest.fixture
def test_settings() -> Settings:
    return Settings(
        APP_ENV="test",
        APP_VERSION="test",
        LOG_LEVEL="INFO",
        MODEL_NAME="tabularisai/multilingual-sentiment-analysis",
        MODEL_TASK="text-classification",
        MAX_INPUT_CHARS=5000,
        MODEL_LOAD_ON_STARTUP=False,
    )


@pytest.fixture
def sentiment_service(test_settings: Settings) -> SentimentService:
    service = SentimentService(test_settings, pipeline_factory=lambda *_args, **_kwargs: fake_pipeline)
    service.load_model()
    return service


@pytest.fixture
def client(
    test_settings: Settings,
    sentiment_service: SentimentService,
) -> Generator[TestClient, None, None]:
    app = create_app(settings=test_settings, sentiment_service=sentiment_service)
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def not_ready_client(test_settings: Settings) -> Generator[TestClient, None, None]:
    service = SentimentService(test_settings, pipeline_factory=lambda *_args, **_kwargs: fake_pipeline)
    app = create_app(settings=test_settings, sentiment_service=service)
    with TestClient(app) as test_client:
        yield test_client

