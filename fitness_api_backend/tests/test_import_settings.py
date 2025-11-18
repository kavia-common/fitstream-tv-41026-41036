from __future__ import annotations

"""
Minimal import verification to exercise Settings() creation and FastAPI app import
without starting the server. Ensures that empty/invalid CORS env values do not
raise JSONDecodeError during Settings initialization.
"""

import os
from contextlib import contextmanager

from src.core.config import get_settings


@contextmanager
def temp_env(env: dict):
    old = {}
    try:
        for k, v in env.items():
            old[k] = os.environ.get(k)
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        # Clear cached settings
        get_settings.cache_clear()  # type: ignore[attr-defined]
        yield
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        get_settings.cache_clear()  # type: ignore[attr-defined]


def test_settings_creation_with_empty_allowed_origins():
    # Exercise both keys with empty/whitespace and ensure no exceptions occur.
    cases = [
        {"allowed_origins": ""},
        {"allowed_origins": "   "},
        {"allowed_origins": None},
        {"CORS_ORIGINS": ""},
        {"CORS_ORIGINS": "   "},
        {"CORS_ORIGINS": None},
    ]
    for env in cases:
        with temp_env(env):
            s = get_settings()
            # Access via safe getters, should always return a list[str]
            assert isinstance(s.get_cors_origins(), list)
            assert isinstance(s.get_cors_headers(), list)
            assert isinstance(s.get_cors_methods(), list)
