from fastapi import APIRouter, Depends, Request

from app.api.dependencies import get_sentiment_service
from app.schemas.sentiment import SentimentRequest, SentimentResponse
from app.services.sentiment_service import SentimentService

router = APIRouter(prefix="/v1", tags=["sentiment"])


@router.post(
    "/sentiment",
    response_model=SentimentResponse,
)
def analyze_sentiment(
    payload: SentimentRequest,
    request: Request,
    service: SentimentService = Depends(get_sentiment_service),
) -> SentimentResponse:
    request_id = getattr(request.state, "request_id", None)
    return service.analyze_sentiment(payload, request_id=request_id)

