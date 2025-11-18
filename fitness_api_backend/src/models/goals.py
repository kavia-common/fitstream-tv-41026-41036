from __future__ import annotations

from typing import Optional
from sqlmodel import SQLModel, Field


class Goal(SQLModel, table=True):
    """Minimal goals model placeholder."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    description: str
    target_per_week: int = Field(default=3)
    is_active: bool = Field(default=True)
