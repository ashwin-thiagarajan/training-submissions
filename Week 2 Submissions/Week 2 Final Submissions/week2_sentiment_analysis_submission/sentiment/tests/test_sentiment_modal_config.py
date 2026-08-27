import os

import pytest
import requests
from requests.auth import HTTPBasicAuth

# Target API URL
API_URL = "http://127.0.0.1:8000/api/v1/sentiment-analysis/"
AUTH = HTTPBasicAuth("api-user", "change-this-api-password")

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_LIVE_SENTIMENT_TESTS") != "true",
    reason="Live sentiment model tests require a running API and model service.",
)

# 5 distinct test cases targeted to trigger each Tabularis.AI sentiment class
SENTIMENT_TEST_DATA = [
    (
        "Very Positive",
        "This is hands down the best product I have ever owned! Pure perfection!",
    ),
    (
        "Positive",
        "The product works well and meets my expectations. Good quality overall.",
    ),
    (
        "Neutral",
        "The package arrived in a standard cardboard box with one unit inside.",
    ),
    (
        "Negative",
        "The quality is quite disappointing and it struggles to function properly.",
    ),
    (
        "Very Negative",
        "ABSOLUTELY TERRIBLE! Complete garbage, total scam, completely broken! Avoid at all costs!",
    ),
]


@pytest.mark.parametrize("expected_sentiment, text_input", SENTIMENT_TEST_DATA)
def test_sentiment_analysis_classes(expected_sentiment, text_input):
    """
    Tests the Django Sentiment Analysis endpoint against all 5 Tabularis.AI classes.
    """
    payload = {"text": text_input}
    headers = {"Content-Type": "application/json"}

    response = requests.post(API_URL, json=payload, headers=headers, auth=AUTH)

    assert (
        response.status_code == 200
    ), f"Expected 200 OK, got {response.status_code}: {response.text}"

    data = response.json()

    assert "text" in data
    assert "sentiment" in data
    assert "score" in data

    assert data["text"] == text_input
    assert 0.0 <= data["score"] <= 1.0

    assert (
        data["sentiment"] == expected_sentiment
    ), f"Expected '{expected_sentiment}' for text '{text_input}', but got '{data['sentiment']}' (score: {data['score']})"


def test_sentiment_analysis_invalid_payload():
    """
    Tests Pydantic validation (min_length rule) returning an error status code.
    """
    payload = {"text": "a"}  # Fails min_length=2 validation
    response = requests.post(
        API_URL, json=payload, headers={"Content-Type": "application/json"}, auth=AUTH
    )

    assert response.status_code == 400