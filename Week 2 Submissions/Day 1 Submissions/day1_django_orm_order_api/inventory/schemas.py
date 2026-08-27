from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, StrictStr

class ProductInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sku: StrictStr = Field(min_length=2, max_length=30)
    name: StrictStr = Field(min_length=2, max_length=100)
    category: StrictStr = Field(min_length=2, max_length=50)
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0)

class CustomerInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: StrictStr = Field(min_length=2, max_length=50)
    last_name: StrictStr = Field(min_length=2, max_length=50)
    email: EmailStr
    phone_number: StrictStr | None = Field(default=None, min_length=7, max_length=15)
    address: StrictStr | None = Field(default=None, min_length=5, max_length=200)

class OrderItemInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_id: int
    quantity: int = Field(gt=0)

class OrderInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: int
    items: list[OrderItemInput]
    status: StrictStr | None = Field(default="Pending", min_length=2, max_length=20)