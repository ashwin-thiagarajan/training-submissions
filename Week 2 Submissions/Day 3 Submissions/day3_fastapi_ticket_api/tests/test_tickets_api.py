from fastapi.testclient import TestClient
from app.main import app
from app.api.dependencies import get_ticket_classifier
from app.core.exceptions import TicketClassificationError
from app.schemas.tickets import TicketClassifyRequest

client = TestClient(app)


def valid_ticket(**overrides):
    payload = {
        "title": "Customer login issue",
        "description": "Customers cannot sign in after the latest deployment.",
        "customer_tier": "STANDARD",
        "affected_users": 10,
        "system_down": False,
    }
    payload.update(overrides)
    return payload

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


def test_system_down_returns_critical_sre() -> None:
    response = client.post("/api/v1/tickets/classify", json=valid_ticket(system_down=True))

    assert response.status_code == 200
    assert response.json()["priority"] == "CRITICAL"
    assert response.json()["recommended_team"] == "SRE"


def test_enterprise_returns_high_priority() -> None:
    response = client.post("/api/v1/tickets/classify", json=valid_ticket(customer_tier="ENTERPRISE"))

    assert response.status_code == 200
    assert response.json()["priority"] == "HIGH"


def test_premium_returns_medium_priority() -> None:
    response = client.post("/api/v1/tickets/classify", json=valid_ticket(customer_tier="PREMIUM"))

    assert response.status_code == 200
    assert response.json()["priority"] == "MEDIUM"


def test_standard_returns_low_priority() -> None:
    response = client.post("/api/v1/tickets/classify", json=valid_ticket())

    assert response.status_code == 200
    assert response.json()["priority"] == "LOW"
    assert response.json()["recommended_team"] == "SUPPORT"


def test_health_returns_200() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_extra_ticket_field_returns_422() -> None:
    response = client.post("/api/v1/tickets/classify", json=valid_ticket(unexpected=True))

    assert response.status_code == 422


def test_classification_failure_returns_structured_500() -> None:
    def failing_classifier(payload: TicketClassifyRequest):
        raise TicketClassificationError()

    def classifier_dependency():
        return failing_classifier

    app.dependency_overrides[get_ticket_classifier] = classifier_dependency
    try:
        response = client.post("/api/v1/tickets/classify", json=valid_ticket())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "API_ERROR",
            "message": "Ticket classification failed.",
            "details": [],
        }
    }

