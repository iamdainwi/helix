# Entry point of the FastAPI application.
# Responsibilities:
#   - Create the FastAPI app instance
#   - Register all feature routers with prefixes and tags
#   - Add global middleware (CORS, logging)
#   - Lifespan: create DB tables on startup

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base

# Import all models so SQLAlchemy registers them before create_all
from app.users.models import User  # noqa: F401
from app.credits.models import CreditLedger  # noqa: F401
from app.brands.models import BrandDNA  # noqa: F401

from app.auth.routes import router as auth_router
from app.users.routes import router as users_router
from app.credits.routes import router as credits_router
from app.brands.routes import router as brands_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create all DB tables if they don't exist
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: nothing to clean up for SQLite


app = FastAPI(
    title="Brand DNA API",
    description="Paste a website URL — get back a complete Brand DNA for your design team.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Feature routers
app.include_router(auth_router,    prefix="/auth",    tags=["Authentication"])
app.include_router(users_router,   prefix="/users",   tags=["Users"])
app.include_router(credits_router, prefix="/credits", tags=["Credits"])
app.include_router(brands_router,  prefix="/brands",  tags=["Brands"])


@app.get("/", tags=["Root"])
def home():
    return {"message": "Brand DNA API — see /docs for full API reference"}


@app.get("/health", tags=["Root"])
def health():
    return {"status": "ok"}