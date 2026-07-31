# Credits schemas — Pydantic models for credit request/response shapes.
# Responsibilities:
#   - Define response shape for balance and history endpoints
#   - Define request shape for credit top-up
#
# Classes:
#   - BalanceOut     : balance field
#   - LedgerEntryOut : id, amount, reason, created_at
#   - TopupRequest   : amount to add (validated: 1–1000)

from pydantic import BaseModel, Field
from datetime import datetime


class BalanceOut(BaseModel):
    balance: int


class LedgerEntryOut(BaseModel):
    id: int
    amount: int
    reason: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TopupRequest(BaseModel):
    amount: int = Field(..., ge=1, le=1000, description="Credits to add (1–1000)")
    reason: str = Field(default="manual_topup")
