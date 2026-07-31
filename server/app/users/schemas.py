# Users schemas — Pydantic models for user request/response shapes.
# Responsibilities:
#   - Define UserOut for serializing user data in responses
#   - Future: UpdateProfileRequest for PATCH /users/me
#
# Classes:
#   - UserOut : id, email, is_active, created_at

from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
