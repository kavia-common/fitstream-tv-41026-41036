from __future__ import annotations

from typing import Optional
from sqlmodel import SQLModel, Field


class Workout(SQLModel, table=True):
    """Minimal workouts model placeholder."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    duration_minutes: int = Field(default=0)
    calories_estimate: int = Field(default=0)
