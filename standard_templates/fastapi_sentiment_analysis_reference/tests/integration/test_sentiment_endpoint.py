from app.services.sentiment_service import SentimentService


def test_sentiment_endpoint_returns_success_payload(client) -> None:
    response = client.post(
        "/v1/sentiment",
        json={"text": "Servicio excelente, really helpful support."},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"]
    body = response.json()
    assert body["label"] == "positive"
    assert body["request_id"] == response.headers["X-Request-ID"]


def test_sentiment_endpoint_rejects_empty_text(client) -> None:
    response = client.post("/v1/sentiment", json={"text": "   "})

    assert response.status_code == 400
    assert response.json()["error_code"] == "validation_error"


def test_sentiment_endpoint_rejects_unknown_fields(client) -> None:
    response = client.post(
        "/v1/sentiment",
        json={"text": "Valid text", "unknown": "value"},
    )

    assert response.status_code == 400
    assert response.json()["error_code"] == "validation_error"


def test_sentiment_endpoint_rejects_oversized_text(client) -> None:
    response = client.post("/v1/sentiment", json={"text": "x" * 5001})

    assert response.status_code == 400
    assert response.json()["error_code"] == "validation_error"


def test_sentiment_endpoint_returns_model_not_ready(not_ready_client) -> None:
    response = not_ready_client.post("/v1/sentiment", json={"text": "hello"})

    assert response.status_code == 500
    assert response.json()["error_code"] == "model_not_ready"


def test_sentiment_endpoint_returns_inference_failed(client, monkeypatch) -> None:
    service: SentimentService = client.app.state.sentiment_service
    service.state.model_pipeline = lambda _text: [{"label": "UNKNOWN", "score": 0.5}]

    response = client.post("/v1/sentiment", json={"text": "hello"})

    assert response.status_code == 500
    assert response.json()["error_code"] == "inference_failed"

