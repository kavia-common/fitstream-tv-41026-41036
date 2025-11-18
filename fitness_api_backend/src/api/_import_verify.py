"""
Utility script to verify that the FastAPI app can be imported without raising
JSONDecodeError or other exceptions due to environment-based settings parsing.

Run:
    python -m src.api._import_verify

This should print a confirmation line and exit(0).
"""
from __future__ import annotations

import sys

try:
    # Importing app forces settings to load and CORS config to be applied
    from src.api.main import app  # noqa: F401
    from src.core.config import get_settings

    settings = get_settings()
    # Print minimal confirmation and the computed CORS origins length (non-sensitive)
    origins = settings.get_cors_origins()
    print(f"OK import. CORS_ORIGINS(len)={len(origins)}")
    sys.exit(0)
except Exception as exc:
    # Avoid printing secrets; show only exception type and message
    print(f"IMPORT_FAILED: {exc.__class__.__name__}: {exc}", file=sys.stderr)
    sys.exit(1)
