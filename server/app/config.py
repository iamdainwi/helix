# Application configuration via environment variables.
# Responsibilities:
#   - Load and validate all env vars using Pydantic BaseSettings
#   - Single source of truth for secrets and config values
#   - Provide a `settings` singleton imported everywhere
#
# Fields:
#   - DATABASE_URL              : SQLite (dev) or Postgres (prod) connection string
#   - SECRET_KEY                : used for JWT signing
#   - ACCESS_TOKEN_EXPIRE_MINUTES : JWT expiry
#   - OLLAMA_CLOUD_HOST         : Ollama Cloud API base URL (https://ollama.com)
#   - OLLAMA_API_KEY            : Bearer token from ollama.com/settings/keys
#   - OLLAMA_MODEL              : Cloud model to use (default: gpt-oss:120b)
#   - FREE_CREDITS_ON_SIGNUP    : credits seeded when a new user registers
#   - PAYMENT_PROVIDER          : "stripe" or "razorpay" — used in production top-up

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./brand_dna.db")

    # Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    # Ollama Cloud
    OLLAMA_CLOUD_HOST: str = os.getenv("OLLAMA_CLOUD_HOST", "https://ollama.com")
    OLLAMA_API_KEY: str = os.getenv("OLLAMA_API_KEY", "")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "deepseek-v4-pro:cloud")

    # Hugging Face (for image generation)
    HF_API_KEY: str = os.getenv("HF_API_KEY", "")
    HF_MODEL: str = os.getenv("HF_MODEL", "black-forest-labs/FLUX.1-dev")
    # HF_MODEL: str = os.getenv("HF_MODEL", "krea/Krea-2-Turbo")

    # Gemini (for image generation fallback)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Credits
    FREE_CREDITS_ON_SIGNUP: int = int(os.getenv("FREE_CREDITS_ON_SIGNUP", 10))

    # Payment (future)
    PAYMENT_PROVIDER: str = os.getenv("PAYMENT_PROVIDER", "stripe")  # "stripe" | "razorpay"

    class Config:
        env_file = ".env"
        extra = "ignore"   # silently skip unknown env vars (e.g. from old .env)

settings = Settings()
