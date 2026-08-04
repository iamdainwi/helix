# Entry point of the FastAPI application.
# Responsibilities:
#   - Create the FastAPI app instance
#   - Register all feature routers with prefixes and tags
#   - Add global middleware (CORS, logging)
#   - Lifespan: create DB tables on startup

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Convert Pydantic's 422 array-style errors into a single human-readable string.
    Without this, the frontend receives [{loc, msg, type}, ...] which renders as [object Object].
    """
    errors = exc.errors()
    # Pick the first meaningful message
    if errors:
        first = errors[0]
        field = " -> ".join(str(loc) for loc in first.get("loc", []) if loc != "body")
        msg = first.get("msg", "Invalid input")
        detail = f"{field}: {msg}" if field else msg
    else:
        detail = "Invalid input"
    return JSONResponse(status_code=422, content={"detail": detail})

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