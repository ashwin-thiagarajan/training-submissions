def test_health_endpoint_ready(client) -> None:
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_health_endpoint_not_ready(not_ready_client) -> None:
    response = not_ready_client.get("/health/ready")

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"

