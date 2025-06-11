"""
Main API router that combines all endpoint routers.
"""

from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, habits, analytics

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(habits.router, prefix="/habits", tags=["habits"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

