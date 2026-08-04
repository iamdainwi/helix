# Credits model — ledger table for tracking credit transactions.
# Responsibilities:
#   - Every credit deduction or top-up is a new row (ledger pattern)
#   - Balance is always computed as SUM(amount) for a user
#   - Reason field tracks which feature consumed the credit
#
# Class:
#   - CreditLedger : id, user_id, amount (+/-), reason, created_at

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Uuid
from datetime import datetime
import uuid
from app.database import Base

class CreditLedger(Base):
    __tablename__ = "credit_ledger"

    id         = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    user_id    = Column(Uuid, ForeignKey("users.id"), nullable=False, index=True)
    amount     = Column(Integer, nullable=False)   # negative = deduction, positive = topup
    reason     = Column(String, nullable=False)    # e.g. "brand_dna_generation", "topup"
    created_at = Column(DateTime, default=datetime.utcnow)
