# Database connection and session management.
# Responsibilities:
#   - Create the SQLAlchemy engine pointing to NeonDB (Postgres) via DATABASE_URL
#   - Provide a declarative Base for all models to inherit from
#   - Provide get_db() dependency for injecting DB sessions into routes
#
# Functions:
#   - get_db() : yields a SQLAlchemy Session, used as FastAPI Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# NeonDB (Postgres) requires pool_pre_ping to handle idle connection drops
# and does NOT need the SQLite-specific check_same_thread arg.
_is_sqlite = settings.DATABASE_URL.startswith("sqlite")
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if _is_sqlite else {},
    pool_pre_ping=not _is_sqlite,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
