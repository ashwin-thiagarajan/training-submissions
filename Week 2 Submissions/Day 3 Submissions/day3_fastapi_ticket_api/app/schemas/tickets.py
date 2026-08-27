from enum import Enum
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerTier(str, Enum):
    FREE = "FREE"
    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"
    ENTERPRISE = "ENTERPRISE"

class TickettPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class TicketRecommendedTeam(str, Enum):
    SUPPORT = "SUPPORT"
    ENGINEERING = "ENGINEERING"
    SRE = "SRE"


class TicketClassifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=5, max_length=120)
    description: str = Field(min_length=20, max_length=5000)
    customer_tier: CustomerTier
    affected_users: int = Field(ge=1, le=100000)
    system_down: bool

class TicketClassifyResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    priority: TickettPriority
    recommended_team: TicketRecommendedTeam
    reasons : list[str] = Field(min_length=1, max_length=5)

