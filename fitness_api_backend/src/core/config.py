from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration using Pydantic BaseSettings.

    Values are loaded from environment variables and .env file if present.
    SECURITY: Do not log sensitive values. Default values are safe for local dev.
    """

    # Pydantic v2 settings configuration:
    # - Read from .env
    # - Ignore unknown/extra environment variables to avoid startup failures
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

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
    # Accept common extra env keys safely (optional use by app/middleware if needed)
    allowed_origins: List[str] = Field(
        default_factory=lambda: ["*"],
        description="Alias/compat: allowed origins list (lowercase key).",
    )
    allowed_headers: List[str] = Field(
        default_factory=lambda: ["*"],
        description="Alias/compat: allowed headers list.",
    )
    allowed_methods: List[str] = Field(
        default_factory=lambda: ["*"],
        description="Alias/compat: allowed methods list.",
    )
    cors_max_age: int = Field(
        default=600,
        description="Alias/compat: CORS preflight cache max age seconds.",
    )

    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./fitness.db",
        description="SQLAlchemy/SQLModel database URL; default is local SQLite file",
    )


# PUBLIC_INTERFACE
@lru_cache
def get_settings() -> Settings:
    """
    Return singleton Settings instance loaded from environment/.env.

    Notes:
        Unknown environment variables are ignored (extra='ignore') to prevent
        Pydantic Settings ValidationError when non-modeled keys are provided.
    """
    return Settings()
