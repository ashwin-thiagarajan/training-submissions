from django.urls import path
from .views import (
    CustomerCreateView,
    ProductCreateView,
    OrderCreateView,
    OrderDetailView,
    OrderByCustomerView,
)

urlpatterns = [
    # Creation endpoints
    path("customers/", CustomerCreateView.as_view(), name="customer-create"),
    path("products/", ProductCreateView.as_view(), name="product-create"),
    path("orders/", OrderCreateView.as_view(), name="order-create"),
    
    # Detail and listing endpoints (fixing minor typo "orderas" -> "orders")
    path("orders/<int:order_id>/", OrderDetailView.as_view(), name="order-detail"),
    path("customers/<int:customer_id>/orders/", OrderByCustomerView.as_view(), name="order-by-customer"),
]

