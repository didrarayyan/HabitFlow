"""
Habit schemas for request/response validation.
"""

from typing import Optional, List
from pydantic import BaseModel, validator
from datetime import datetime, date

from app.models.habit import HabitType, HabitFrequency


class HabitBase(BaseModel):
    """Base habit schema."""
    name: str
    description: Optional[str] = None
    habit_type: HabitType = HabitType.BOOLEAN
    frequency: HabitFrequency = HabitFrequency.DAILY
    target_value: float = 1.0
    unit: Optional[str] = None
    icon: str = "🎯"
    color: str = "#3B82F6"
    reminder_enabled: bool = False
    reminder_time: Optional[str] = None

    @validator("color")
    def validate_color(cls, v):
        """Validate hex color format."""
        if not v.startswith("#") or len(v) != 7:
            raise ValueError("Color must be in hex format (#RRGGBB)")
        return v

    @validator("reminder_time")
    def validate_reminder_time(cls, v):
        """Validate time format."""
        if v is not None:
            try:
                hour, minute = v.split(":")
                if not (0 <= int(hour) <= 23 and 0 <= int(minute) <= 59):
                    raise ValueError("Invalid time format")
            except (ValueError, AttributeError):
                raise ValueError("Time must be in HH:MM format")
        return v


class HabitCreate(HabitBase):
    """Habit creation schema."""
    pass


class HabitUpdate(BaseModel):
    """Habit update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    habit_type: Optional[HabitType] = None
    frequency: Optional[HabitFrequency] = None
    target_value: Optional[float] = None
    unit: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None
    reminder_enabled: Optional[bool] = None
    reminder_time: Optional[str] = None

    @validator("color")
    def validate_color(cls, v):
        """Validate hex color format."""
        if v is not None and (not v.startswith("#") or len(v) != 7):
            raise ValueError("Color must be in hex format (#RRGGBB)")
        return v

    @validator("reminder_time")
    def validate_reminder_time(cls, v):
        """Validate time format."""
        if v is not None:
            try:
                hour, minute = v.split(":")
                if not (0 <= int(hour) <= 23 and 0 <= int(minute) <= 59):
                    raise ValueError("Invalid time format")
            except (ValueError, AttributeError):
                raise ValueError("Time must be in HH:MM format")
        return v


class HabitInDBBase(HabitBase):
    """Base habit schema with database fields."""
    id: int
    is_active: bool
    current_streak: int
    longest_streak: int
    total_completions: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int

    class Config:
        orm_mode = True


class Habit(HabitInDBBase):
    """Habit schema for responses."""
    pass


class HabitWithStats(Habit):
    """Habit schema with additional statistics."""
    completion_rate: Optional[float] = None
    recent_entries: Optional[List["HabitEntry"]] = None


# Habit entry schemas
class HabitEntryBase(BaseModel):
    """Base habit entry schema."""
    date: date
    completed: bool = False
    value: Optional[float] = None
    notes: Optional[str] = None


class HabitEntryCreate(HabitEntryBase):
    """Habit entry creation schema."""
    habit_id: int


class HabitEntryUpdate(BaseModel):
    """Habit entry update schema."""
    completed: Optional[bool] = None
    value: Optional[float] = None
    notes: Optional[str] = None


class HabitEntryInDBBase(HabitEntryBase):
    """Base habit entry schema with database fields."""
    id: int
    habit_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class HabitEntry(HabitEntryInDBBase):
    """Habit entry schema for responses."""
    pass


# Analytics schemas
class HabitAnalytics(BaseModel):
    """Habit analytics schema."""
    habit_id: int
    habit_name: str
    total_days: int
    completed_days: int
    completion_rate: float
    current_streak: int
    longest_streak: int
    average_value: Optional[float] = None


class DashboardStats(BaseModel):
    """Dashboard statistics schema."""
    total_habits: int
    active_habits: int
    today_completed: int
    today_total: int
    current_streak: int
    total_completions: int

