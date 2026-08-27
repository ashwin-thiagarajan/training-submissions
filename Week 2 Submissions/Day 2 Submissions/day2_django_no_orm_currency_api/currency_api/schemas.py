from pydantic import BaseModel, Field, field_validator, ConfigDict

class ConversionRequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    amount: float = Field(..., description="Amount to be converted")
    from_currency: str = Field(..., min_length=3, max_length=3)
    to_currency: str = Field(..., min_length=3, max_length=3)

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Amount must be greater than 0.")
        if round(value, 2) != value:
            raise ValueError("Amount must have at most 2 decimal places.")
        return value
    @field_validator("from_currency", "to_currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()
    
class ConversionResponseSchema(BaseModel):
    amount: float = Field(..., description="Original amount")
    converted_amount: float = Field(..., description="Converted amount")
    from_currency: str = Field(..., min_length=3, max_length=3)
    to_currency: str = Field(..., min_length=3, max_length=3)
    rate: float = Field(..., description="Conversion rate used for the conversion")

    @field_validator('converted_amount')
    @classmethod
    def format_two_decimal_places(cls, value: float) -> float:
        return round(value, 2)