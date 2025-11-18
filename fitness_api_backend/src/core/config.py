from __future__ import annotations

from functools import lru_cache
from typing import List, Optional

from pydantic import Field, ConfigDict, AnyUrl, HttpUrl
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

    # SECURITY (critical fields must exist but have safe dev defaults)
    SECRET_KEY: str = Field(
        default="change-this-in-production",
        description="Secret key for signing JWTs; must be overridden in production via .env",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60 * 24, description="JWT access token expiry in minutes"
    )

    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./fitness.db",
        description="SQLAlchemy/SQLModel database URL; default is local SQLite file",
    )

    # CORS (primary used by app)
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: ["*"],
        description="Allowed origins for CORS; use specific origins in production",
    )

    # Compat/common environment variables often present in deployments.
    # They are optional and used by other tooling; defined here to avoid extra-key errors
    # and to provide typed, safe defaults. The app currently doesn't require them, but
    # exposing them enables future use and prevents Settings ValidationError.
    backend_url: Optional[HttpUrl] = Field(
        default=None, description="Public base URL for backend (if provided by env)"
    )
    frontend_url: Optional[HttpUrl] = Field(
        default=None, description="Public base URL for frontend (if provided by env)"
    )
    site_url: Optional[HttpUrl] = Field(
        default=None, description="Canonical site URL used for redirects (if provided)"
    )
    ws_url: Optional[AnyUrl] = Field(
        default=None, description="WebSocket base URL (ws:// or wss://) if provided"
    )

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
    cookie_domain: Optional[str] = Field(
        default=None, description="Domain to set on cookies if needed (e.g., .example.com)"
    )
    trust_proxy: bool = Field(
        default=False,
        description="Whether the app trusts proxy headers like X-Forwarded-For/Proto.",
    )

    # Server/runtime hints
    host: str = Field(default="0.0.0.0", description="App host bind for internal use")
    uvicorn_host: str = Field(
        default="0.0.0.0", description="Host for uvicorn when starting server"
    )
    uvicorn_workers: int = Field(
        default=1, description="Number of workers for uvicorn/gunicorn"
    )
    port: int = Field(default=8000, description="Port to bind the server to")
    node_env: str = Field(
        default="development",
        description="Environment name hint often used by frontends (development/production).",
    )

    # Request/limits
    request_timeout_ms: int = Field(
        default=30000, description="Default request timeout in milliseconds"
    )
    rate_limit_window_s: int = Field(
        default=60, description="Rate limit window seconds (if used by middleware)"
    )
    rate_limit_max: int = Field(
        default=100, description="Maximum requests per window per client (if used)"
    )

    # Back-compat aliases mapping: if CORS_ORIGINS is not explicitly set, derive from allowed_origins
    def get_cors_origins(self) -> List[str]:
        """
        Provide a unified CORS origins list prioritizing CORS_ORIGINS.
        Falls back to allowed_origins if CORS_ORIGINS is left default and allowed_origins differs.
        """
        if self.CORS_ORIGINS and self.CORS_ORIGINS != ["*"]:
            return self.CORS_ORIGINS
        if self.allowed_origins and self.allowed_origins != ["*"]:
            return self.allowed_origins
        return self.CORS_ORIGINS


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
