# Credits controller — business logic for credit balance and transactions.
# Responsibilities:
#   - Compute balance via SUM on ledger
#   - Return transaction history for a user
#   - deduct_credit() is called by other feature controllers (brands, etc.)
#
# Functions:
#   - get_balance(user_id, db)              : returns {"balance": int}
#   - get_history(user_id, db)              : returns list of ledger rows
#   - deduct_credit(db, user_id, reason)    : inserts -1 row into ledger
#   - topup_credit(db, user_id, amount)     : inserts +N row into ledger

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.credits.models import CreditLedger
import uuid

def get_balance(user_id: uuid.UUID, db: Session):
    balance = db.query(func.sum(CreditLedger.amount))\
                .filter(CreditLedger.user_id == user_id)\
                .scalar() or 0
    return {"balance": balance}

def get_history(user_id: uuid.UUID, db: Session):
    return db.query(CreditLedger)\
             .filter(CreditLedger.user_id == user_id)\
             .order_by(CreditLedger.created_at.desc())\
             .all()

def deduct_credit(db: Session, user_id: uuid.UUID, reason: str, amount: int = 1):
    entry = CreditLedger(user_id=user_id, amount=-amount, reason=reason)
    db.add(entry)
    # caller is responsible for db.commit()

def topup_credit(db: Session, user_id: uuid.UUID, amount: int, reason: str = "topup"):
    entry = CreditLedger(user_id=user_id, amount=amount, reason=reason)
    db.add(entry)
    # caller is responsible for db.commit()
