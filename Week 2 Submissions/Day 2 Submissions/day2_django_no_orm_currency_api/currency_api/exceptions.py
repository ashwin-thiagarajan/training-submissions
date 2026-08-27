class CurrencyServiceError(Exception):
    """Base class for expected currency-service failures."""


class UnsupportedCurrencyError(CurrencyServiceError):
    """Raised when a currency is not in the configured rate table."""


class SameCurrencyError(CurrencyServiceError):
    """Raised when source and target currencies are identical."""
