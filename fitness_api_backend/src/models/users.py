from __future__ import annotations

from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """
    Minimal user model placeholder to unblock imports.

    Fields may be extended later with auth/profile attributes.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = Field(default=True)
