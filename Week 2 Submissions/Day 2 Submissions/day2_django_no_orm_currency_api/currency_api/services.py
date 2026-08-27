from .exceptions import SameCurrencyError, UnsupportedCurrencyError
from .schemas import ConversionResponseSchema

CONVERSION_RATES: dict[str, float] = {
    "USD": 1.0,
    "EUR": 0.85,
    "GBP": 0.75,
    "INR": 74.0,
    "JPY": 110.0,
}

def convert_currency(amount: float, from_currency: str, to_currency: str) -> ConversionResponseSchema:
    if from_currency == to_currency:
        raise SameCurrencyError("Source and target currencies must be different.")
    if from_currency not in CONVERSION_RATES or to_currency not in CONVERSION_RATES:
        raise UnsupportedCurrencyError("Invalid currency code.")
    
    rate = CONVERSION_RATES[from_currency]
    target_rate = CONVERSION_RATES[to_currency]
    converted_amount = round((amount * target_rate) / rate , 2)
    actual_rate = round(target_rate / rate, 2)

    return ConversionResponseSchema(
        amount=round(amount, 2),
        converted_amount=converted_amount,
        from_currency=from_currency,
        to_currency=to_currency,
        rate=actual_rate
    )