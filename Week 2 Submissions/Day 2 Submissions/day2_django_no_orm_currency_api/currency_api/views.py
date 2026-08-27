import json
import logging
from json import JSONDecodeError
from typing import Any

from pydantic import ValidationError
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .schemas import ConversionRequestSchema
from .exceptions import CurrencyServiceError
from .services import convert_currency

logger = logging.getLogger(__name__)


def error_response(code: str, message: str, details: list[Any] | None = None) -> dict:
    return {"error": {"code": code, "message": message, "details": details or []}}


class ConvertCurrencyView(APIView):
    def post(self, request: Request) -> Response:
        try:
            payload = ConversionRequestSchema.model_validate(request.data)
            result = convert_currency(
                payload.amount, payload.from_currency, payload.to_currency
            )
        except (ParseError, JSONDecodeError):
            return Response(
                error_response("INVALID_JSON", "Malformed JSON request body."),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as exc:
            sanitized_errors = json.loads(exc.json(include_url=False))
            return Response(
                error_response(
                    "VALIDATION_ERROR",
                    "Invalid request payload.",
                    sanitized_errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except CurrencyServiceError as exc:
            logger.warning("Currency conversion rejected: %s", exc)
            return Response(
                error_response("VALIDATION_ERROR", str(exc)),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            logger.exception("Currency conversion execution failed")
            return Response(
                error_response("INTERNAL_ERROR", "Internal server error."),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        logger.info("Currency conversion completed successfully")
        return Response(result.model_dump(), status=status.HTTP_200_OK)