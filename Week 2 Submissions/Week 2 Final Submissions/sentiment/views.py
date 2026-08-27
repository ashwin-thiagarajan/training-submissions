import logging

from pydantic import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import ModelInferenceError
from .schemas import SentimentRequest
from .services import get_sentiment_service

logger = logging.getLogger(__name__)


def error_response(code: str, message: str, details: list | None = None) -> dict:
    return {"error": {"code": code, "message": message, "details": details or []}}


class HealthView(APIView):
    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class SentimentAnalysisView(APIView):
    def post(self, request):
        try:
            payload = SentimentRequest.model_validate(request.data)
            result = get_sentiment_service().analyze(payload)
        except ValidationError as exc:
            return Response(
                error_response("VALIDATION_ERROR", "Invalid request payload.", exc.errors()),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ModelInferenceError:
            logger.exception("Sentiment inference failed")
            return Response(
                error_response("MODEL_INFERENCE_ERROR", "Unable to analyze sentiment."),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        logger.info("Sentiment analysis completed")
        return Response(result.model_dump(), status=status.HTTP_200_OK)

