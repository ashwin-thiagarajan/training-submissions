from app.schemas.tickets import TicketClassifyRequest, TicketClassifyResponse, CustomerTier, TicketPriority, TicketRecommendedTeam

def classify_ticket(payload: TicketClassifyRequest) -> TicketClassifyResponse:
    if payload.system_down:
        priority = TicketPriority.CRITICAL
        recommended_team = TicketRecommendedTeam.SRE
        reasons = ["System is down"]
    elif payload.affected_users > 1000:
        priority = TicketPriority.HIGH
        recommended_team = TicketRecommendedTeam.ENGINEERING
        reasons = ["High number of affected users"]
    elif payload.customer_tier == CustomerTier.ENTERPRISE:
        priority = TicketPriority.HIGH
        recommended_team = TicketRecommendedTeam.SUPPORT
        reasons = ["Enterprise customer"]
    elif payload.customer_tier == CustomerTier.PREMIUM:
        priority = TicketPriority.MEDIUM
        recommended_team = TicketRecommendedTeam.SUPPORT
        reasons = ["Premium customer"]
    else:
        priority = TicketPriority.LOW
        recommended_team = TicketRecommendedTeam.SUPPORT
        reasons = ["Standard or Free customer"]
    return TicketClassifyResponse(
        priority=priority,
        recommended_team=recommended_team,
        reasons=reasons
    )