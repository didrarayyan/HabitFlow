"""
Dependencies for API endpoints.
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import security
from app.core.database import get_db
from app.models.user import User
from app.services.user_service import UserService


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(security.oauth2_scheme)
) -> User:
    """Get current authenticated user."""
    user_id = security.verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_service = UserService(db)
    user = user_service.get(id=int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    return current_user

