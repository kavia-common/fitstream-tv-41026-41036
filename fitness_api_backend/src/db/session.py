from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlmodel import SQLModel, Session, create_engine

from src.core.config import get_settings

# Create engine based on settings
_settings = get_settings()
# For SQLite, check_same_thread must be False when using in async web servers via threads
_engine = create_engine(
    _settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if _settings.DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=True,
)


# PUBLIC_INTERFACE
def get_engine():
    """Return the global SQLModel engine instance."""
    return _engine


# PUBLIC_INTERFACE
def get_session() -> Session:
    """Return a new SQLModel Session bound to the app engine."""
    return Session(_engine)


@contextmanager
def session_scope() -> Iterator[Session]:
    """
    Provide a transactional scope around a series of operations.

    Commits on success, rollbacks on exceptions, and always closes the session.
    """
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# PUBLIC_INTERFACE
def init_db(create_all: bool = True) -> None:
    """
    Initialize database at application startup.

    If create_all is True, will create all tables defined in SQLModel metadata.
    """
    if create_all:
        # Import models to ensure they are registered with SQLModel metadata
        from src.db import base as _  # noqa: F401  # side-effect import
        SQLModel.metadata.create_all(bind=_engine)
