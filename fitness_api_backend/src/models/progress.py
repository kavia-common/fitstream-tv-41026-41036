from __future__ import annotations

from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field


class Progress(SQLModel, table=True):
    """Minimal progress model placeholder."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    workout_id: Optional[int] = Field(default=None, index=True)
    on_date: date = Field(default_factory=date.today)
    calories_burned: int = Field(default=0)
    duration_minutes: int = Field(default=0)
