# Users controller — business logic for user profile operations.
# Responsibilities:
#   - Return serialized user profile
#   - Future: update profile, change password
#
# Functions:
#   - get_profile(user) : returns user data dict

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.users.models import User
from app.users.schemas import UserUpdate
from app.auth.utils import hash_password

def get_profile(user: User):
    return {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": user.created_at,
    }

def update_profile(user: User, data: UserUpdate, db: Session):
    if data.email and data.email != user.email:
        # Check if email is already taken
        existing_user = db.query(User).filter(User.email == data.email).first()
        if existing_user:
            raise HTTPException(400, "Email already in use")
        user.email = data.email

    if data.password:
        user.hashed_password = hash_password(data.password)

    db.commit()
    db.refresh(user)
    return get_profile(user)
