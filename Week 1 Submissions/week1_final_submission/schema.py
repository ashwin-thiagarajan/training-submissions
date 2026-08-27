from typing import Literal
from pydantic import BaseModel, EmailStr, Field, ValidationError

class Customer(BaseModel):
    customer_id : int
    name : str = Field(min_length=2,pattern="^[a-zA-Z\s]+$")
    email : EmailStr

class Product(BaseModel):
    product_id : int
    name: str = Field(min_length=2,pattern="^[a-zA-Z\s]+$")
    category: str
    price: int = Field(gt=0)
    stock: int = Field(ge=0)

class OrderItem(BaseModel):
    order_item_id: int
    product: Product
    quantity: int = Field(gt=0)
    discount: float = Field(ge=0, lt=100, default =0)

class Order(BaseModel):
    order_id : int
    customer: Customer
    items: list[OrderItem] = Field(min_length=1)
    status: Literal["PLACED", "PAID", "SHIPPED", "CANCELLED"] = "PLACED"

def main():
    print("--- 1. Testing Valid Order Definition ---")
    try:
        valid_order = Order(
            order_id=101,
            customer={"customer_id": 1, "name": "Alice Smith", "email": "alice@example.com"},
            items=[
                {
                    "order_item_id": 1,
                    "product": {
                        "product_id": 500,
                        "name": "Laptop",
                        "category": "Electronics",
                        "price": 1200,
                        "stock": 15
                    },
                    "quantity": 1,
                    "discount": 10.0
                }
            ],
            status="PLACED"
        )
        print("Success! Valid order created:")
        print(valid_order.model_dump_json(indent=2))
        
    except ValidationError as e:
        print("Validation failed unexpectedly:", e)

    print("\n--- 2. Testing Invalid Order Definition ---")
    try:
        invalid_order = Order(
            order_id=102,
            customer={"customer_id": 2, "name": "Bob123", "email": "not-an-email"},
            items=[],
            status="PENDING"  
        )
        print("Success! Invalid order created (this shouldn't print).")
        
    except ValidationError as e:
        print("Validation caught expected errors:")
        for error in e.errors():
            field = " -> ".join(str(loc) for loc in error["loc"])
            print(f"  * Field [{field}]: {error['msg']} (Type: {error['type']})")

if __name__ == "__main__":
    main()