from collections.abc import Callable

from app.schemas.tickets import TicketClassifyRequest, TicketClassifyResponse
from app.services.tickets import classify_ticket

TicketClassifier = Callable[[TicketClassifyRequest], TicketClassifyResponse]


def get_ticket_classifier() -> TicketClassifier:
    return classify_ticket
