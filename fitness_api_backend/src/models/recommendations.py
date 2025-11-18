from __future__ import annotations

from typing import Optional
from sqlmodel import SQLModel, Field


class Recommendation(SQLModel, table=True):
    """Minimal recommendations model placeholder."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    workout_id: int = Field(index=True)
    reason: str = ""
