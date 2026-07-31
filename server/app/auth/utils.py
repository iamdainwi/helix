# Auth utilities — pure helper functions for JWT and password operations.
# Responsibilities:
#   - Hash and verify passwords using bcrypt
#   - Encode and decode JWT tokens using python-jose
#   - No DB interaction, no HTTP — pure functions only
#
# Functions:
#   - hash_password(plain)          : returns bcrypt hash
#   - verify_password(plain, hashed): returns bool
#   - create_access_token(data)     : returns signed JWT string
#   - decode_access_token(token)    : returns payload dict or raises

from datetime import datetime, timedelta
from jose import jwt, JWTError
import bcrypt
from fastapi import HTTPException
from app.config import settings

def hash_password(plain: str) -> str:
    # bcrypt returns bytes, we decode to string for the DB column
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False

def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(401, "Invalid or expired token")
