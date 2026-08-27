from fastapi import APIRouter, Depends, Response, status

from app.api.dependencies import get_sentiment_service
from app.schemas.health import ReadinessResponse
from app.services.sentiment_service import SentimentService

router = APIRouter(tags=["health"])


@router.get(
    "/health/ready",
    response_model=ReadinessResponse,
    responses={503: {"model": ReadinessResponse}},
)
def get_readiness(
    response: Response,
    service: SentimentService = Depends(get_sentiment_service),
) -> ReadinessResponse:
    readiness = service.readiness()
    if not readiness.model_loaded:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return readiness

