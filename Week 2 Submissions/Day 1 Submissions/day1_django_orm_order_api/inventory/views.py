import logging
from django.db import IntegrityError
from rest_framework.request import Request
from pydantic import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order
from .serializers import (
    CustomerSerializer, 
    ProductSerializer, 
    OrderDetailSerializer
)
from .services import (
    create_customer,
    create_product,
    create_order_with_items,
    get_order,
    get_order_for_customer,
    InsufficientStockError,
    OrderNotFoundError,
    ObjectDoesNotExist
)

logger = logging.getLogger(__name__)


def error_response(code: str, message: str, details: list | None = None) -> dict:
    return {"error": {"code": code, "message": message, "details": details or []}}

class CustomerCreateView(APIView):
    def post(self, request: Request) -> Response:
        try:
            customer = create_customer(request.data)
            serializer = CustomerSerializer(customer)
            logger.info(f"Customer created successfully: ID {customer.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as exc:
            logger.info("Customer validation failed")
            return Response(error_response("VALIDATION_ERROR", "Invalid request payload.", exc.errors()), status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            logger.warning("Customer creation conflicted with an existing record")
            return Response(error_response("DUPLICATE_RESOURCE", "A customer with that email already exists."), status=status.HTTP_409_CONFLICT)
        except Exception:
            logger.exception("Failed to create customer")
            return Response(error_response("INTERNAL_ERROR", "Internal server error."), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductCreateView(APIView):
    def post(self, request: Request) -> Response:
        try:
            product = create_product(request.data)
            serializer = ProductSerializer(product)
            logger.info(f"Product created successfully: ID {product.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as exc:
            logger.info("Product validation failed")
            return Response(error_response("VALIDATION_ERROR", "Invalid request payload.", exc.errors()), status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            logger.warning("Product creation conflicted with an existing SKU")
            return Response(error_response("DUPLICATE_RESOURCE", "A product with that SKU already exists."), status=status.HTTP_409_CONFLICT)
        except Exception:
            logger.exception("Failed to create product")
            return Response(error_response("INTERNAL_ERROR", "Internal server error."), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderCreateView(APIView):
    def post(self, request: Request) -> Response:
        try:
            order = create_order_with_items(request.data)
            serializer = OrderDetailSerializer(order)
            logger.info(f"Order created successfully: ID {order.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except InsufficientStockError as e:
            logger.warning(f"Stock conflict: {str(e)}")
            return Response({
                "error": {
                    "code": "STATE_CONFLICT",
                    "message": str(e),
                    "details": []
                }
            }, status=status.HTTP_409_CONFLICT)
            
        except ObjectDoesNotExist as e:
            logger.warning(f"Resource missing: {str(e)}")
            return Response({   
                "error": {
                    "code": "RESOURCE_NOT_FOUND",
                    "message": str(e),
                    "details": []
                }
            }, status=status.HTTP_404_NOT_FOUND)
            
        except ValidationError as exc:
            logger.info("Order validation failed")
            return Response(error_response("VALIDATION_ERROR", "Invalid request payload.", exc.errors()), status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logger.exception("Order creation failed")
            return Response(error_response("INTERNAL_ERROR", "Internal server error."), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderDetailView(APIView):
    def get(self, request: Request, order_id: int) -> Response:
        try:
            # Applying select_related and prefetch_related for optimal query performance
            order = get_order(order_id)
            serializer = OrderDetailSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OrderNotFoundError:
            logger.warning("Order detail requested for missing ID: %s", order_id)
            return Response(error_response("RESOURCE_NOT_FOUND", "The requested order was not found."), status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            logger.warning(f"Order detail requested for missing ID: {order_id}")
            return Response(error_response("RESOURCE_NOT_FOUND", "The requested order was not found."), status=status.HTTP_404_NOT_FOUND)


class OrderByCustomerView(APIView):
    def get(self, request: Request, customer_id: int) -> Response:
        try:
            orders = get_order_for_customer(customer_id)
            if not orders:
                return Response(error_response("RESOURCE_NOT_FOUND", "No orders were found for this customer."), status=status.HTTP_404_NOT_FOUND)
            
            serializer = OrderDetailSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, OrderNotFoundError):
            logger.warning("Orders requested for missing customer %s", customer_id)
            return Response(error_response("RESOURCE_NOT_FOUND", "The requested customer was not found."), status=status.HTTP_404_NOT_FOUND)
        except Exception:
            logger.exception("Error fetching orders for customer %s", customer_id)
            return Response(error_response("INTERNAL_ERROR", "Internal server error."), status=status.HTTP_500_INTERNAL_SERVER_ERROR)