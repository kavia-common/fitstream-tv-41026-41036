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
        # Restore
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        get_settings.cache_clear()  # type: ignore[attr-defined]


def test_empty_and_whitespace_values_do_not_raise():
    cases = [None, "", "   "]
    for val in cases:
        with temp_env({"CORS_ORIGINS": val, "allowed_origins": val}):
            settings = get_settings()
            origins = settings.get_cors_origins()
            assert isinstance(origins, list)


def test_csv_values_parsed_safely():
    with temp_env({"CORS_ORIGINS": "http://a.com, https://b.com , *"}):
        settings = get_settings()
        origins = settings.get_cors_origins()
        assert origins == ["http://a.com", "https://b.com", "*"]


def test_json_array_values_parsed_safely():
    with temp_env({"CORS_ORIGINS": '["https://x.com","https://y.com"]'}):
        settings = get_settings()
        origins = settings.get_cors_origins()
        assert origins == ["https://x.com", "https://y.com"]


def test_malformed_json_falls_back_to_csv():
    with temp_env({"CORS_ORIGINS": "[invalid,json"}):
        settings = get_settings()
        origins = settings.get_cors_origins()
        # Fallback to CSV split by comma
        assert origins == ["[invalid", "json"]


def test_methods_and_headers_also_return_lists():
    with temp_env(
        {
            "allowed_methods": "GET, POST,PUT",
            "allowed_headers": '["Authorization","Content-Type"]',
        }
    ):
        s = get_settings()
        assert s.get_cors_methods() == ["GET", "POST", "PUT"]
        assert s.get_cors_headers() == ["Authorization", "Content-Type"]
