"""
Aggregate SQLModel models for metadata registration.

Import all model modules here so that SQLModel.metadata.create_all can discover them.
Keep models light and avoid heavy logic in module import stage.
"""

# flake8: noqa F401
from src.models.users import User  # placeholder model
from src.models.workouts import Workout  # placeholder model
from src.models.progress import Progress  # placeholder model
from src.models.goals import Goal  # placeholder model
from src.models.badges import Badge  # placeholder model
from src.models.recommendations import Recommendation  # placeholder model
from src.models.ratings import Rating  # placeholder model
