from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration using Pydantic BaseSettings.

    Values are loaded from environment variables and .env file if present.
    SECURITY: Do not log sensitive values. Default values are safe for local dev.
    """

    # SECURITY
    SECRET_KEY: str = Field(
        default="change-this-in-production",
        description="Secret key for signing JWTs; must be overridden in production via .env",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60 * 24, description="JWT access token expiry in minutes"
    )

    # CORS
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: ["*"],
        description="Allowed origins for CORS; use specific origins in production",
    )

    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./fitness.db",
        description="SQLAlchemy/SQLModel database URL; default is local SQLite file",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# PUBLIC_INTERFACE
@lru_cache
def get_settings() -> Settings:
    """Return singleton Settings instance loaded from environment/.env."""
    return Settings()
