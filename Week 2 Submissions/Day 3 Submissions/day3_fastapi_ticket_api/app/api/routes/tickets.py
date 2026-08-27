import logging

from fastapi import APIRouter, status

from app.schemas.tickets import TicketClassifyRequest, TicketClassifyResponse
from app.services.tickets import classify_ticket

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post(
    "/classify",
    response_model=TicketClassifyResponse,
    status_code=status.HTTP_200_OK,
)
def classify_ticket_endpoint(payload: TicketClassifyRequest) -> TicketClassifyResponse:
    result = classify_ticket(payload)
    logger.info("Ticket classified", extra={"priority": result.priority})
    return result

