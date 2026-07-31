# Database connection and session management.
# Responsibilities:
#   - Create the SQLAlchemy engine pointing to SQLite (or swap to Postgres later)
#   - Provide a declarative Base for all models to inherit from
#   - Provide get_db() dependency for injecting DB sessions into routes
#
# Functions:
#   - get_db() : yields a SQLAlchemy Session, used as FastAPI Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite only
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
