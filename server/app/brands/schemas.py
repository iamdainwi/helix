# Brands schemas — Pydantic models for brand DNA request/response shapes.
# Responsibilities:
#   - Validate incoming URL from client
#   - Define response shape for brand DNA records
#   - dna is deserialized from a JSON string stored in DB to a dict in responses
#
# Classes:
#   - BrandRequest  : url field (validated as HttpUrl)
#   - BrandDNAOut   : id, user_id, url, dna (dict), created_at

from pydantic import BaseModel, HttpUrl, field_validator
from datetime import datetime
import json


class BrandRequest(BaseModel):
    url: HttpUrl


class BrandDNAOut(BaseModel):
    id: int
    user_id: int
    url: str
    dna: dict          # deserialized from JSON string stored in DB
    created_at: datetime

    model_config = {"from_attributes": True}

    @field_validator("dna", mode="before")
    @classmethod
    def parse_dna(cls, v):
        """Convert stored JSON string to dict for API responses."""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return {}
        return v or {}
