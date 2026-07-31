# Auth controller — business logic for authentication.
# Responsibilities:
#   - Handle user registration (check duplicate, hash password, insert)
#   - Seed FREE_CREDITS_ON_SIGNUP credits for every new user
#   - Handle user login (verify password, issue JWT)
#   - Raise appropriate HTTPExceptions for bad input
#
# Functions:
#   - register(body, db) : creates user, seeds credits, returns token
#   - login(body, db)    : validates credentials, returns token

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.users.models import User
from app.auth.schemas import RegisterRequest, LoginRequest
from app.auth.utils import hash_password, verify_password, create_access_token
from app.credits.controller import topup_credit
from app.config import settings

async def register(body: RegisterRequest, db: Session):
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(400, "Email already registered")

    user = User(email=body.email, hashed_password=hash_password(body.password))
    db.add(user)
    db.flush()  # assign user.id without committing yet

    # Seed free credits for new user
    topup_credit(db, user.id, amount=settings.FREE_CREDITS_ON_SIGNUP, reason="signup_bonus")

    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


async def login(body: LoginRequest, db: Session):
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
