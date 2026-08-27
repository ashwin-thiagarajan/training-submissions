from app.schemas.tickets import TicketClassifyRequest,CustomerTier
from app.services.tickets import classify_ticket


def test_calculate_ticket_score() -> None:
    payload = TicketClassifyRequest(
        title="High Impact User Issue",
        description="Users across multiple regions are reporting login timeouts during authentication.",
        customer_tier=CustomerTier.PREMIUM,
        affected_users=2500,
        system_down=False,
    )

    result = classify_ticket(payload)

    assert result.priority == "HIGH"
    assert result.recommended_team == "ENGINEERING"
    assert "High number of affected users" in result.reasons

