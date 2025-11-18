from __future__ import annotations

from typing import Optional
from sqlmodel import SQLModel, Field


class Badge(SQLModel, table=True):
    """Minimal badges model placeholder."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str = ""
