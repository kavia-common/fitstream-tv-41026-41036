"""
Run a quick Uvicorn import check to verify that the ASGI app import path is valid.
This does not start a long-running server; it imports and builds the app, then exits.

Usage:
    python uvicorn_import_check.py
"""
from uvicorn.importer import import_from_string


def main() -> int:
    # Import the FastAPI app using Uvicorn's importer
    # This will raise if import path is broken due to settings parsing.
    app = import_from_string("src.api.main:app")  # noqa: F841
    print("Uvicorn import check OK: src.api.main:app")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
