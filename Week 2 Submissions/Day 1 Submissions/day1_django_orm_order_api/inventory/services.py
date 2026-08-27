from django.db import transaction
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from .models import Product,Customer,Order,OrderItem
from .schemas import ProductInput,CustomerInput,OrderInput,OrderItemInput

class OrderNotFoundError(Exception):
    pass
class InsufficientStockError(Exception):
    pass

def create_customer(data:dict)->Customer:
    payload = CustomerInput.model_validate(data)
    return Customer.objects.create(**payload.model_dump())

def create_product(data:dict)->Product:
    payload = ProductInput.model_validate(data)
    return Product.objects.create(**payload.model_dump())

@transaction.atomic
def create_order_with_items(data:dict)->Order:
    payload = OrderInput.model_validate(data)
    try:
        customer = Customer.objects.get(id=payload.customer_id)
    except Customer.DoesNotExist as exc:
        raise ObjectDoesNotExist(f"Customer {payload.customer_id} not found.") from exc

    order = Order.objects.create(customer=customer, total_amount=0, status=payload.status)
    total_amount = 0
    for item_data in payload.items:
        try:
            product = Product.objects.select_for_update().get(id=item_data.product_id)
        except Product.DoesNotExist as exc:
            raise ObjectDoesNotExist(f"Product {item_data.product_id} not found.") from exc

        if product.stock < item_data.quantity:
            raise InsufficientStockError(
                f"Insufficient stock for {product.name}. Requested: {item_data.quantity}, Available: {product.stock}"
            )

        product.stock = F('stock') - item_data.quantity
        product.save(update_fields=['stock'])

        item_price = product.price
        total_amount += product.price * item_data.quantity

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item_data.quantity,
            price=item_price
        )
        order.total_amount = total_amount
        order.save(update_fields=['total_amount'])
    return order

def get_order(order_id:int)->Order:
    try:
        return Order.objects.get(id=order_id)
    except ObjectDoesNotExist as exc:
        raise OrderNotFoundError("Order not found.") from exc

def get_order_for_customer(customer_id:int)->list[Order]:
    try:
        return list(Order.objects.filter(customer_id=customer_id))
    except ObjectDoesNotExist as exc:
        raise OrderNotFoundError("Order not found for the customer.") from exc