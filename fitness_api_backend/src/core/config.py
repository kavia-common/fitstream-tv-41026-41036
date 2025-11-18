from __future__ import annotations

import json
from functools import lru_cache
from typing import List, Optional, Any

from pydantic import Field, ConfigDict, AnyUrl, HttpUrl, field_validator
from pydantic_settings import BaseSettings


def _parse_list_like(value: object) -> List[str]:
    """
    Safely parse list-like configuration values coming from environment variables.

    Supports:
      - JSON arrays (e.g., '["*"]', '["http://a","https://b"]')
      - Comma-separated strings (e.g., 'http://a, https://b , *')
      - Empty strings or None -> []
      - Already-typed lists -> list[str] with str-cast and trimming

    Never raises on invalid JSON; falls back to comma-splitting. Ensures all
    items are unique, trimmed strings, and skips empty items.
    """
    if value is None:
        return []

    # If already a list/tuple, coerce to cleaned list[str]
    if isinstance(value, (list, tuple, set)):
        cleaned: List[str] = []
        seen = set()
        for item in value:
            s = str(item).strip()
            if s and s not in seen:
                cleaned.append(s)
                seen.add(s)
        return cleaned

    if isinstance(value, str):
        s = value.strip()
        if s == "":
            return []
        # Try JSON array first only if string appears to be a JSON array
        if s.startswith("[") and s.endswith("]"):
            try:
                parsed = json.loads(s)
                if isinstance(parsed, (list, tuple)):
                    return _parse_list_like(parsed)
            except json.JSONDecodeError:
                # If JSON invalid, fall through to CSV parsing
                pass

        # Fallback: comma-separated values
        parts = [p.strip() for p in s.split(",")]
        cleaned = [p for p in parts if p]
        # Deduplicate while preserving order
        unique: List[str] = []
        seen = set()
        for item in cleaned:
            if item not in seen:
                unique.append(item)
                seen.add(item)
        return unique

    # Unknown type, cast to string and attempt CSV style
    return _parse_list_like(str(value))


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
    # Accept raw env values which could be JSON arrays or comma separated strings.
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: ["*"],
        description="Allowed origins for CORS; use specific origins in production",
    )

    # Compat/common environment variables often present in deployments.
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

    # Common aliases used in various deployments
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

    # Validators to ensure robust parsing when env provides strings (including empty)
    @field_validator("CORS_ORIGINS", "allowed_origins", "allowed_headers", "allowed_methods", mode="before")
    @classmethod
    def _coerce_list_env(cls, v: Any) -> Any:
        """
        Coerce environment-provided values for list fields into list[str].

        Handles:
          - None or "" -> []
          - JSON arrays -> parsed list
          - CSV strings -> list
          - Already lists/tuples/sets -> normalized list[str]
        """
        parsed = _parse_list_like(v)
        return parsed

    # PUBLIC_INTERFACE
    def get_cors_origins(self) -> List[str]:
        """
        Provide a unified CORS origins list prioritizing CORS_ORIGINS.

        Supports env inputs that may be JSON arrays, comma-separated strings, or empty strings.
        Falls back to allowed_origins if CORS_ORIGINS is effectively default and allowed_origins differs.

        Returns:
            List[str]: computed origins list for FastAPI CORSMiddleware.
        """
        cors_origins = _parse_list_like(self.CORS_ORIGINS)
        allowed_origins = _parse_list_like(self.allowed_origins)

        # If explicit CORS_ORIGINS provided (not empty and not ["*"] by intention), prefer it
        if cors_origins and cors_origins != ["*"]:
            return cors_origins

        # Else, if allowed_origins provided specifically, use it
        if allowed_origins and allowed_origins != ["*"]:
            return allowed_origins

        # Safe default permissive wildcard for local/dev
        return cors_origins or ["*"]

    # Convenience helpers for headers and methods
    def get_cors_headers(self) -> List[str]:
        """
        Return parsed allowed headers list with robust handling of env formats.
        """
        headers = _parse_list_like(self.allowed_headers)
        return headers or ["*"]

    def get_cors_methods(self) -> List[str]:
        """
        Return parsed allowed methods list with robust handling of env formats.
        """
        methods = _parse_list_like(self.allowed_methods)
        return methods or ["*"]


# PUBLIC_INTERFACE
@lru_cache
def get_settings() -> Settings:
    """
    Return singleton Settings instance loaded from environment/.env.

    Notes:
        Unknown environment variables are ignored (extra='ignore') to prevent
        Pydantic Settings ValidationError when non-modeled keys are provided.

    Security:
        Do not print or log the settings contents to avoid leaking secrets.
    """
    return Settings()
