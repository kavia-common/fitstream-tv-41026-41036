from __future__ import annotations

from typing import Optional
from sqlmodel import SQLModel, Field


class Rating(SQLModel, table=True):
    """Minimal ratings model placeholder."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    workout_id: int = Field(index=True)
    score: int = Field(ge=1, le=5, default=5)
    comment: str = ""
