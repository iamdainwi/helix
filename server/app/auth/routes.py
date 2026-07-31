# Auth routes — all HTTP route declarations for authentication.
# Responsibilities:
#   - Define /auth/register and /auth/login endpoints
#   - Validate request bodies via schemas
#   - Delegate all logic to auth/controller.py
#
# Routes:
#   - POST /auth/register : create new user account
#   - POST /auth/login    : verify credentials, return JWT

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import schemas, controller

router = APIRouter()

@router.post("/register")
async def register(body: schemas.RegisterRequest, db: Session = Depends(get_db)):
    return await controller.register(body, db)

@router.post("/login")
async def login(body: schemas.LoginRequest, db: Session = Depends(get_db)):
    return await controller.login(body, db)
