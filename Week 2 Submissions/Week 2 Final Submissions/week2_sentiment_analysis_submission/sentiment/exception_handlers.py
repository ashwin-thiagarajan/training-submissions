from typing import Any

from rest_framework.views import exception_handler


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Any:
    response = exception_handler(exc, context)
    if response is None:
        return None

    if response.status_code == 401:
        response.data = {
            "error": {
                "code": "AUTHENTICATION_REQUIRED",
                "message": "Authentication credentials are required or invalid.",
                "details": [],
            }
        }
    return response
