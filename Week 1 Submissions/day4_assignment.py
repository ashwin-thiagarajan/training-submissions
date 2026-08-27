from typing import Literal
from pydantic import BaseModel, EmailStr, Field

class Product(BaseModel):
    product_id : int
    name: str
    category: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)

class Customer(BaseModel):
    customer_id: int
    name: str = Field(min_length=2,pattern="^[a-zA-Z\s]+$")
    country: str
    email: EmailStr

class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: float

class Order(BaseModel):
    customer_id: int
    items: list[OrderItem] = Field(min_length=1)
    status: Literal["PLACED", "PAID", "SHIPPED", "CANCELLED"] = "PLACED"

if __name__ == "__main__":

    try:
        print(Customer(
            customer_id=1, name="John Doe", country="USA", email="john.doeexample.com"
        ))
    except Exception as e:
        print(f"Failed: {e}")

    try:
        print(Customer(
            customer_id=2, name="Jane Smith", country="Canada", email="john.smith@example.com"
        ))
    except Exception as e:
        print(f"Failed: {e}")

    try:
        print(Order(
            customer_id=1, 
            items=[OrderItem(product_id=1, quantity=3, unit_price=10.0)], 
            status="PLACED"
        ))
    except Exception as e:
        print(f"Failed: {e}")

    try:
        print(Order(
            customer_id=2, items=[]
        ))
    except Exception as e:
        print(f"Failed: {e}")