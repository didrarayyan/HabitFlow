"""
Analytics endpoints for dashboard statistics and habit analytics.
"""

from typing import Any, List, Dict
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.core.database import get_db
from app.models.user import User
from app.models.habit import Habit
from app.models.habit_entry import HabitEntry
from app.schemas.habit import HabitAnalytics, DashboardStats
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get dashboard statistics for current user."""
    today = date.today()
    
    # Total habits
    total_habits = db.query(Habit).filter(Habit.owner_id == current_user.id).count()
    
    # Active habits
    active_habits = db.query(Habit).filter(
        and_(Habit.owner_id == current_user.id, Habit.is_active == True)
    ).count()
    
    # Today's entries
    today_entries = db.query(HabitEntry).filter(
        and_(HabitEntry.user_id == current_user.id, HabitEntry.date == today)
    ).all()
    
    today_completed = sum(1 for entry in today_entries if entry.completed)
    today_total = len(today_entries)
    
    # Current streak (longest current streak among all habits)
    habits = db.query(Habit).filter(Habit.owner_id == current_user.id).all()
    current_streak = max((habit.current_streak for habit in habits), default=0)
    
    # Total completions
    total_completions = db.query(func.sum(Habit.total_completions)).filter(
        Habit.owner_id == current_user.id
    ).scalar() or 0
    
    return DashboardStats(
        total_habits=total_habits,
        active_habits=active_habits,
        today_completed=today_completed,
        today_total=today_total,
        current_streak=current_streak,
        total_completions=total_completions,
    )


@router.get("/habits", response_model=List[HabitAnalytics])
def get_habit_analytics(
    db: Session = Depends(get_db),
    days: int = Query(30, description="Number of days to analyze"),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get analytics for all user habits."""
    start_date = date.today() - timedelta(days=days)
    
    habits = db.query(Habit).filter(Habit.owner_id == current_user.id).all()
    analytics = []
    
    for habit in habits:
        # Get entries for the specified period
        entries = db.query(HabitEntry).filter(
            and_(
                HabitEntry.habit_id == habit.id,
                HabitEntry.date >= start_date
            )
        ).all()
        
        total_days = days
        completed_days = sum(1 for entry in entries if entry.completed)
        completion_rate = (completed_days / total_days) * 100 if total_days > 0 else 0
        
        # Calculate average value for count/duration habits
        average_value = None
        if habit.habit_type in ["count", "duration"]:
            values = [entry.value for entry in entries if entry.value is not None]
            average_value = sum(values) / len(values) if values else 0
        
        analytics.append(HabitAnalytics(
            habit_id=habit.id,
            habit_name=habit.name,
            total_days=total_days,
            completed_days=completed_days,
            completion_rate=completion_rate,
            current_streak=habit.current_streak,
            longest_streak=habit.longest_streak,
            average_value=average_value,
        ))
    
    return analytics


@router.get("/habits/{habit_id}/calendar")
def get_habit_calendar_data(
    *,
    db: Session = Depends(get_db),
    habit_id: int,
    year: int = Query(None, description="Year for calendar data"),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get calendar heatmap data for a specific habit."""
    # Verify habit ownership
    habit = db.query(Habit).filter(
        and_(Habit.id == habit_id, Habit.owner_id == current_user.id)
    ).first()
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Default to current year if not specified
    if year is None:
        year = date.today().year
    
    # Get all entries for the year
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    
    entries = db.query(HabitEntry).filter(
        and_(
            HabitEntry.habit_id == habit_id,
            HabitEntry.date >= start_date,
            HabitEntry.date <= end_date
        )
    ).all()
    
    # Create calendar data
    calendar_data = {}
    for entry in entries:
        date_str = entry.date.isoformat()
        calendar_data[date_str] = {
            "completed": entry.completed,
            "value": entry.value,
            "notes": entry.notes,
        }
    
    return {
        "habit_id": habit_id,
        "habit_name": habit.name,
        "year": year,
        "data": calendar_data,
    }


@router.get("/habits/{habit_id}/progress")
def get_habit_progress(
    *,
    db: Session = Depends(get_db),
    habit_id: int,
    days: int = Query(30, description="Number of days for progress data"),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get progress data for a specific habit."""
    # Verify habit ownership
    habit = db.query(Habit).filter(
        and_(Habit.id == habit_id, Habit.owner_id == current_user.id)
    ).first()
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Get entries for the specified period
    start_date = date.today() - timedelta(days=days)
    
    entries = db.query(HabitEntry).filter(
        and_(
            HabitEntry.habit_id == habit_id,
            HabitEntry.date >= start_date
        )
    ).order_by(HabitEntry.date).all()
    
    # Create progress data
    progress_data = []
    for entry in entries:
        progress_data.append({
            "date": entry.date.isoformat(),
            "completed": entry.completed,
            "value": entry.value,
            "target": habit.target_value,
        })
    
    return {
        "habit_id": habit_id,
        "habit_name": habit.name,
        "habit_type": habit.habit_type,
        "target_value": habit.target_value,
        "unit": habit.unit,
        "progress": progress_data,
    }

