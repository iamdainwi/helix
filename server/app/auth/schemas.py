# Auth schemas — Pydantic models for auth request/response validation.
# Responsibilities:
#   - Define shape of incoming request bodies for register and login
#   - Define shape of token response
#
# Classes:
#   - RegisterRequest : email + password for new user
#   - LoginRequest    : email + password for login
#   - TokenResponse   : access_token + token_type

from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
