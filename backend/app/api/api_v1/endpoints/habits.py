"""
Habit endpoints for habit and habit entry management.
"""

from typing import Any, List
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.habit import Habit
from app.schemas.habit import (
    Habit as HabitSchema,
    HabitCreate,
    HabitUpdate,
    HabitEntry as HabitEntrySchema,
    HabitEntryCreate,
    HabitEntryUpdate,
)
from app.services.habit_service import HabitService, HabitEntryService
from app.api.deps import get_current_active_user

router = APIRouter()


# Habit endpoints
@router.get("/", response_model=List[HabitSchema])
def read_habits(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    active_only: bool = Query(False, description="Filter only active habits"),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Retrieve habits for current user."""
    habit_service = HabitService(db)
    
    if active_only:
        habits = habit_service.get_active_by_user(user_id=current_user.id)
    else:
        habits = habit_service.get_by_user(
            user_id=current_user.id, skip=skip, limit=limit
        )
    
    return habits


@router.post("/", response_model=HabitSchema)
def create_habit(
    *,
    db: Session = Depends(get_db),
    habit_in: HabitCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Create new habit."""
    habit_service = HabitService(db)
    habit = habit_service.create(obj_in=habit_in, user_id=current_user.id)
    return habit


@router.get("/{habit_id}", response_model=HabitSchema)
def read_habit(
    *,
    db: Session = Depends(get_db),
    habit_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get habit by ID."""
    habit_service = HabitService(db)
    habit = habit_service.get(id=habit_id)
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    if habit.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return habit


@router.put("/{habit_id}", response_model=HabitSchema)
def update_habit(
    *,
    db: Session = Depends(get_db),
    habit_id: int,
    habit_in: HabitUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Update habit."""
    habit_service = HabitService(db)
    habit = habit_service.get(id=habit_id)
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    if habit.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    habit = habit_service.update(db_obj=habit, obj_in=habit_in)
    return habit


@router.delete("/{habit_id}")
def delete_habit(
    *,
    db: Session = Depends(get_db),
    habit_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Delete habit."""
    habit_service = HabitService(db)
    habit = habit_service.get(id=habit_id)
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    if habit.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    habit = habit_service.delete(id=habit_id)
    return {"message": "Habit deleted successfully"}


# Habit entry endpoints
@router.get("/{habit_id}/entries", response_model=List[HabitEntrySchema])
def read_habit_entries(
    *,
    db: Session = Depends(get_db),
    habit_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get habit entries for a specific habit."""
    habit_service = HabitService(db)
    habit = habit_service.get(id=habit_id)
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    if habit.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    entry_service = HabitEntryService(db)
    entries = entry_service.get_by_habit(
        habit_id=habit_id, skip=skip, limit=limit
    )
    
    return entries


@router.post("/entries", response_model=HabitEntrySchema)
def create_habit_entry(
    *,
    db: Session = Depends(get_db),
    entry_in: HabitEntryCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Create new habit entry."""
    habit_service = HabitService(db)
    habit = habit_service.get(id=entry_in.habit_id)
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    if habit.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    entry_service = HabitEntryService(db)
    entry = entry_service.create(obj_in=entry_in, user_id=current_user.id)
    
    # Update habit streak
    habit_service.update_streak(habit)
    
    return entry


@router.get("/entries/{entry_id}", response_model=HabitEntrySchema)
def read_habit_entry(
    *,
    db: Session = Depends(get_db),
    entry_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get habit entry by ID."""
    entry_service = HabitEntryService(db)
    entry = entry_service.get(id=entry_id)
    
    if not entry:
        raise HTTPException(status_code=404, detail="Habit entry not found")
    
    if entry.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return entry


@router.put("/entries/{entry_id}", response_model=HabitEntrySchema)
def update_habit_entry(
    *,
    db: Session = Depends(get_db),
    entry_id: int,
    entry_in: HabitEntryUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Update habit entry."""
    entry_service = HabitEntryService(db)
    entry = entry_service.get(id=entry_id)
    
    if not entry:
        raise HTTPException(status_code=404, detail="Habit entry not found")
    
    if entry.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    entry = entry_service.update(db_obj=entry, obj_in=entry_in)
    
    # Update habit streak
    habit_service = HabitService(db)
    habit = habit_service.get(id=entry.habit_id)
    if habit:
        habit_service.update_streak(habit)
    
    return entry


@router.delete("/entries/{entry_id}")
def delete_habit_entry(
    *,
    db: Session = Depends(get_db),
    entry_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Delete habit entry."""
    entry_service = HabitEntryService(db)
    entry = entry_service.get(id=entry_id)
    
    if not entry:
        raise HTTPException(status_code=404, detail="Habit entry not found")
    
    if entry.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    habit_id = entry.habit_id
    entry = entry_service.delete(id=entry_id)
    
    # Update habit streak
    habit_service = HabitService(db)
    habit = habit_service.get(id=habit_id)
    if habit:
        habit_service.update_streak(habit)
    
    return {"message": "Habit entry deleted successfully"}


@router.get("/entries/date/{entry_date}", response_model=List[HabitEntrySchema])
def read_entries_by_date(
    *,
    db: Session = Depends(get_db),
    entry_date: date,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get all habit entries for a specific date."""
    entry_service = HabitEntryService(db)
    entries = entry_service.get_by_user_and_date(
        user_id=current_user.id, entry_date=entry_date
    )
    
    return entries

