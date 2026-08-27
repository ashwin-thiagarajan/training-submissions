import logging
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
    ObjectDoesNotExist
)

logger = logging.getLogger(__name__)

class CustomerCreateView(APIView):
    def post(self, request):
        try:
            customer = create_customer(request.data)
            serializer = CustomerSerializer(customer)
            logger.info(f"Customer created successfully: ID {customer.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Failed to create customer: {str(e)}")
            return Response({
                "error": {
                    "code": "BAD_REQUEST",
                    "message": "Invalid request payload",
                    "details": [str(e)]
                }       
            }, status=status.HTTP_400_BAD_REQUEST)


class ProductCreateView(APIView):
    def post(self, request):
        try:
            product = create_product(request.data)
            serializer = ProductSerializer(product)
            logger.info(f"Product created successfully: ID {product.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Failed to create product: {str(e)}")
            return Response({
                "error": {
                    "code":"BAD_REQUEST",
                    "message": "Invalid request payload",
                    "details": [str(e)]
                }
            }, status=status.HTTP_400_BAD_REQUEST)


class OrderCreateView(APIView):
    def post(self, request):
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
            
        except Exception as e: # Catches Pydantic ValidationError and others
            logger.error(f"Order creation failed: {str(e)}")
            return Response({
                "error": {
                    "code": "BAD_REQUEST",
                    "message": "Invalid request payload.",
                    "details": [str(e)]
                }
            }, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    def get(self, request, order_id):
        try:
            # Applying select_related and prefetch_related for optimal query performance
            order = Order.objects.select_related('customer').prefetch_related('items__product').get(id=order_id)
            serializer = OrderDetailSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            logger.warning(f"Order detail requested for missing ID: {order_id}")
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)


class OrderByCustomerView(APIView):
    def get(self, request, customer_id):
        try:
            orders = Order.objects.filter(customer_id=customer_id).select_related('customer').prefetch_related('items__product')
            if not orders.exists():
                return Response({"detail": "No orders found for this customer."}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = OrderDetailSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching orders for customer {customer_id}: {str(e)}")
            return Response({
                "error": {
                    "code":"BAD_REQUEST",
                    "message": "Invalid request payload",
                    "details": [str(e)]
                }
            }, status=status.HTTP_400_BAD_REQUEST)