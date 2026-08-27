def test_sentiment_success_contract(client) -> None:
    response = client.post(
        "/v1/sentiment",
        json={"text": "This service is excellent.", "request_id": "req-123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {
        "request_id",
        "label",
        "confidence",
        "model_name",
        "input_size",
        "processed_at",
    }
    assert body["request_id"] == "req-123"
    assert body["label"] == "positive"
    assert 0 <= body["confidence"] <= 1
    assert body["model_name"] == "tabularisai/multilingual-sentiment-analysis"
    assert body["input_size"] > 0


def test_sentiment_validation_error_contract(client) -> None:
    response = client.post("/v1/sentiment", json={"text": ""})

    assert response.status_code == 400
    body = response.json()
    assert set(body) == {
        "request_id",
        "error_code",
        "message",
        "details",
        "retryable",
    }
    assert body["error_code"] == "validation_error"
    assert body["retryable"] is False


def test_sentiment_server_error_contract(not_ready_client) -> None:
    response = not_ready_client.post("/v1/sentiment", json={"text": "hello"})

    assert response.status_code == 500
    body = response.json()
    assert body["error_code"] == "model_not_ready"
    assert body["retryable"] is True


def test_readiness_contract_ready(client) -> None:
    response = client.get("/health/ready")

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"status", "model_loaded", "version", "checked_at"}
    assert body["status"] == "ready"
    assert body["model_loaded"] is True


def test_readiness_contract_not_ready(not_ready_client) -> None:
    response = not_ready_client.get("/health/ready")

    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "not_ready"
    assert body["model_loaded"] is False

