# Users routes — HTTP route declarations for user profile operations.
# Responsibilities:
#   - Define /users/me endpoint (get current user profile)
#   - All routes require authentication via require_auth dependency
#
# Routes:
#   - GET /users/me : return current authenticated user's profile

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import require_auth
from app.users.models import User
from app.users import controller
from app.users import schemas

router = APIRouter()

@router.get("/me", response_model=schemas.UserOut)
async def get_me(current_user: User = Depends(require_auth)):
    return controller.get_profile(current_user)

@router.put("/me", response_model=schemas.UserOut)
async def update_me(
    body: schemas.UserUpdate,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    return controller.update_profile(current_user, body, db)
