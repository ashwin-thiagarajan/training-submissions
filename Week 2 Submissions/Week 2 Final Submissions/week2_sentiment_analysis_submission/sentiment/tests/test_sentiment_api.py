from base64 import b64encode
from unittest.mock import Mock, patch

from django.urls import reverse
from rest_framework.test import APIClient


def authenticated_client() -> APIClient:
    client = APIClient()
    credentials = b64encode(b"api-user:change-this-api-password").decode("ascii")
    client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials}")
    return client


def test_health_returns_200() -> None:
    response = APIClient().get(reverse("health"))

    assert response.status_code == 200


def test_sentiment_request_without_credentials_returns_401() -> None:
    response = APIClient().post(
        reverse("sentiment-analysis"),
        {"text": "I love this product."},
        format="json",
    )

    assert response.status_code == 401


def test_sentiment_request_with_invalid_credentials_returns_401() -> None:
    client = APIClient()
    credentials = b64encode(b"api-user:wrong-password").decode("ascii")
    client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials}")

    response = client.post(
        reverse("sentiment-analysis"),
        {"text": "I love this product."},
        format="json",
    )

    assert response.status_code == 401


def test_valid_sentiment_request_returns_200() -> None:
    service = Mock()
    service.analyze.return_value.model_dump.return_value = {
        "text": "I love this product.",
        "sentiment": "Positive",
        "score": 0.98,
    }

    with patch("sentiment.views.get_sentiment_service", return_value=service):
        response = authenticated_client().post(
            reverse("sentiment-analysis"),
            {"text": "I love this product."},
            format="json",
        )

    assert response.status_code == 200
    assert response.data["sentiment"] == "Positive"


def test_missing_text_returns_400() -> None:
    response = authenticated_client().post(reverse("sentiment-analysis"), {}, format="json")

    assert response.status_code == 400

