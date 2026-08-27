import logging
from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import TicketClassifier, get_ticket_classifier
from app.core.config import Settings, get_settings
from app.core.exceptions import TicketClassificationError
from app.schemas.tickets import TicketClassifyRequest, TicketClassifyResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post(
    "/classify",
    response_model=TicketClassifyResponse,
    status_code=status.HTTP_200_OK,
)
def classify_ticket_endpoint(
    payload: TicketClassifyRequest,
    classifier: TicketClassifier = Depends(get_ticket_classifier),
    settings: Settings = Depends(get_settings),
) -> TicketClassifyResponse:
    try:
        result = classifier(payload)
    except TicketClassificationError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    logger.info("Ticket classified", extra={"priority": result.priority, "environment": settings.app_env})
    return result

