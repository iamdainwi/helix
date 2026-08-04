# Core dependencies — reusable FastAPI Depends functions.
# Responsibilities:
#   - require_auth    : extract JWT from Authorization header, return current User
#   - require_credits : run require_auth, then check credit balance > 0
#   - Used across all protected routes via Depends()
#
# Functions:
#   - require_auth(token, db)    : decodes JWT, fetches user from DB
#   - require_credits(user, db)  : checks balance, raises 402 if insufficient

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.utils import decode_access_token
from app.users.models import User
from app.credits.models import CreditLedger

bearer = HTTPBearer()

async def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db)
) -> User:
    payload = decode_access_token(credentials.credentials)
    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user or not user.is_active:
        raise HTTPException(401, "User not found or inactive")
    return user

async def require_credits(
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
) -> User:
    balance = db.query(func.sum(CreditLedger.amount))\
                .filter(CreditLedger.user_id == current_user.id)\
                .scalar() or 0
    if balance <= 0:
        raise HTTPException(402, "Insufficient credits")
    return current_user
