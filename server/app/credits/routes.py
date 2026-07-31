# Credits routes — HTTP route declarations for credit operations.
# Responsibilities:
#   - Expose endpoints for checking balance, viewing transaction history,
#     and topping up credits
#   - All routes require authentication
#   - POST /credits/topup is currently open to any authenticated user (no payment).
#     In production, this will be hooked into Stripe or Razorpay.
#
# Routes:
#   - GET  /credits/balance : return current credit balance for user
#   - GET  /credits/history : return list of credit transactions
#   - POST /credits/topup   : add credits to user account (no payment for now)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import require_auth
from app.users.models import User
from app.credits import controller, schemas

router = APIRouter()


@router.get("/balance", response_model=schemas.BalanceOut)
async def get_balance(
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db),
):
    return controller.get_balance(current_user.id, db)


@router.get("/history", response_model=list[schemas.LedgerEntryOut])
async def get_history(
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db),
):
    return controller.get_history(current_user.id, db)


@router.post("/topup", response_model=schemas.BalanceOut)
async def topup(
    body: schemas.TopupRequest,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db),
):
    """
    Add credits to the authenticated user's account.
    Currently open without payment validation.
    Production: integrate Stripe/Razorpay webhook before calling topup_credit().
    """
    controller.topup_credit(db, current_user.id, amount=body.amount, reason=body.reason)
    db.commit()
    return controller.get_balance(current_user.id, db)
