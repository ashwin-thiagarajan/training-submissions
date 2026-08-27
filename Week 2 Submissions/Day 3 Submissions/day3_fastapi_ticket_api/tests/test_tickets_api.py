from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_score_ticket_returns_high_priority() -> None:
    response = client.post(
        "/api/v1/tickets/classify",
        json={
            "title": "High Impact User Issue",
            "description": "Users across multiple regions are reporting login timeouts during authentication.",
            "customer_tier": "PREMIUM",
            "affected_users": 2500,
            "system_down": False
        },
    )

    assert response.status_code == 200
    assert response.json()["priority"] == "HIGH"


def test_invalid_ticket_data_returns_422() -> None:
    response = client.post(
        "/api/v1/tickets/classify",
        json={
            "title": "Bad",
            "description": "This is an invalid ticket.",
            "customer_tier": "PREMIUM",
            "affected_users": 2500,
            "system_down": False
        },
    )

    assert response.status_code == 422

