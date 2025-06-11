"""
User endpoints for user management.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate
from app.services.user_service import UserService
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get current user."""
    return current_user


@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Update current user."""
    user_service = UserService(db)
    
    # Check if email is being changed and if it's already taken
    if user_in.email and user_in.email != current_user.email:
        existing_user = user_service.get_by_email(email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )
    
    # Check if username is being changed and if it's already taken
    if user_in.username and user_in.username != current_user.username:
        existing_user = user_service.get_by_username(username=user_in.username)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="The user with this username already exists in the system.",
            )
    
    user = user_service.update(db_obj=current_user, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=UserSchema)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """Get a specific user by id."""
    user_service = UserService(db)
    user = user_service.get(id=user_id)
    
    if user == current_user:
        return user
    
    if not user_service.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    
    return user


@router.delete("/me")
def delete_user_me(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Delete current user."""
    # Deactivate user instead of deleting to preserve data integrity
    user_service = UserService(db)
    user_service.update(
        db_obj=current_user,
        obj_in={"is_active": False}
    )
    return {"message": "User account deactivated successfully"}

