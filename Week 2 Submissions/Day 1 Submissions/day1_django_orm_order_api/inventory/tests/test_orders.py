import pytest
from rest_framework.test import APIClient
from inventory.models import Customer, Product, Order

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def setup_data():
    customer = Customer.objects.create(
        first_name="Jane", 
        last_name="Doe", 
        email="jane.doe@example.com"
    )
    product = Product.objects.create(
        sku="SKU-TEST-1", 
        name="Test Item", 
        category="Test", 
        price=10.00, 
        stock=5
    )
    return {"customer": customer, "product": product}

@pytest.mark.django_db
class TestOrderAPI:
    
    def test_successful_order_creation(self, api_client, setup_data):
        """Test 201 Created and that stock is properly deducted."""
        payload = {
            "customer_id": setup_data["customer"].id,
            "items": [
                {"product_id": setup_data["product"].id, "quantity": 2}
            ]
        }
        
        response = api_client.post("/api/v1/orders/", payload, format="json")
        assert response.status_code == 201
        
        # Verify database state
        order_id = response.data["id"]
        order = Order.objects.get(id=order_id)
        assert order.total_amount == 20.00
        
        # Verify stock was deducted
        setup_data["product"].refresh_from_db()
        assert setup_data["product"].stock == 3

    def test_invalid_payload(self, api_client, setup_data):
        """Test 400 Bad Request for negative quantity."""
        payload = {
            "customer_id": setup_data["customer"].id,
            "items": [
                {"product_id": setup_data["product"].id, "quantity": -5}
            ]
        }
        
        response = api_client.post("/api/v1/orders/", payload, format="json")
        assert response.status_code == 400
        assert "error" in response.data
        assert response.data["error"]["code"] == "VALIDATION_ERROR"

    def test_insufficient_stock(self, api_client, setup_data):
        """Test 409 Conflict when requesting more than available stock."""
        payload = {
            "customer_id": setup_data["customer"].id,
            "items": [
                {"product_id": setup_data["product"].id, "quantity": 10}  # Stock is only 5
            ]
        }
        
        response = api_client.post("/api/v1/orders/", payload, format="json")
        assert response.status_code == 409
        assert "error" in response.data
        assert response.data["error"]["code"] == "STATE_CONFLICT"
        
        # Verify stock was NOT deducted
        setup_data["product"].refresh_from_db()
        assert setup_data["product"].stock == 5

    def test_missing_order_id(self, api_client):
        """Test 404 Not Found for non-existent order."""
        response = api_client.get("/api/v1/orders/9999/")
        assert response.status_code == 404
        assert "error" in response.data