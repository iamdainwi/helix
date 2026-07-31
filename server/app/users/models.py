# Users model — SQLAlchemy table definition for the users table.
# Responsibilities:
#   - Define columns for the users table
#   - Referenced by auth controller for register/login
#   - Referenced by credits and brands via foreign key
#
# Class:
#   - User : id, email, hashed_password, is_active, created_at

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    email           = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active       = Column(Boolean, default=True)
    created_at      = Column(DateTime, default=datetime.utcnow)
