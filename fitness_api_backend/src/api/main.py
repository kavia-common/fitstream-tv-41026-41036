from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.db.session import init_db
from src.api.routes.auth import router as auth_router

settings = get_settings()

app = FastAPI(
    title="FitStream Fitness API",
    description="Backend for user data, workouts, recommendations, progress tracking, and goals.",
    version="0.1.0",
    openapi_tags=[
        {"name": "health", "description": "Service health and diagnostics"},
        {"name": "auth", "description": "Authentication endpoints"},
        {"name": "users", "description": "User profile and settings"},
        {"name": "workouts", "description": "Workout content and metadata"},
        {"name": "progress", "description": "Progress tracking and stats"},
        {"name": "recommendations", "description": "Personalized recommendations"},
        {"name": "goals", "description": "Goals management"},
        {"name": "badges", "description": "Motivational badges"},
        {"name": "ratings", "description": "User ratings for workouts"},
    ],
)

# Configure CORS using settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(auth_router)


@app.on_event("startup")
def _on_startup():
    """
    Application startup hook.
    Initializes database and ensures tables are created (dev-safe).
    """
    init_db(create_all=True)


@app.get("/", tags=["health"], summary="Health Check", description="Simple service health check endpoint that returns a static payload.")
def health_check():
    """
    Health check endpoint to verify the service is operational.

    Returns:
        JSON payload with a message.
    """
    return {"message": "Healthy"}
