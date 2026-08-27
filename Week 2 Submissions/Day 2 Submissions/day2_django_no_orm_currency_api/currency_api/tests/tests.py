import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_convert_currency_success(api_client):
    payload = {"amount": 100.50, "from_currency": "usd", "to_currency": "INR"}
    response = api_client.post("/api/v1/convert-currency/", payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["amount"] == 100.5
    assert data["from_currency"] == "USD"
    assert data["converted_amount"] == 7437.0
    assert data["rate"] == 74.0


@pytest.mark.django_db
def test_convert_currency_extra_fields_forbidden(api_client):
    payload = {
        "amount": 100,
        "from_currency": "USD",
        "to_currency": "INR",
        "extra_field": "disallowed",
    }
    response = api_client.post("/api/v1/convert-currency/", payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.django_db
def test_convert_currency_invalid_decimals(api_client):
    payload = {"amount": 100.555, "from_currency": "USD", "to_currency": "INR"}
    response = api_client.post("/api/v1/convert-currency/", payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.django_db
def test_unsupported_currency(api_client):
    payload = {"amount": 100, "from_currency": "XYZ", "to_currency": "INR"}
    response = api_client.post("/api/v1/convert-currency/", payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.django_db
def test_same_source_and_target_currency(api_client):
    payload = {"amount": 100, "from_currency": "USD", "to_currency": "USD"}
    response = api_client.post("/api/v1/convert-currency/", payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"