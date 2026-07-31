# Brands model — SQLAlchemy table for storing generated Brand DNA records.
# Responsibilities:
#   - Persist every brand DNA result tied to a user
#   - Store raw URL, scraped metadata, and AI-generated DNA as JSON string
#
# Class:
#   - BrandDNA : id, user_id, url, scraped_data (JSON), dna (JSON), created_at

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class BrandDNA(Base):
    __tablename__ = "brand_dna"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    url          = Column(String, nullable=False)
    scraped_data = Column(Text)   # raw scraped content as JSON string
    dna          = Column(Text)   # AI-generated brand DNA as JSON string
    created_at   = Column(DateTime, default=datetime.utcnow)
