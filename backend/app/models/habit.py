"""
Habit model for habit management.
"""

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum

from app.core.database import Base


class HabitType(str, Enum):
    """Habit type enumeration."""
    BOOLEAN = "boolean"  # Yes/No completion
    COUNT = "count"      # Count-based (e.g., 10 push-ups)
    DURATION = "duration"  # Time-based (e.g., 30 minutes)


class HabitFrequency(str, Enum):
    """Habit frequency enumeration."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class Habit(Base):
    """Habit model."""
    
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Habit configuration
    habit_type = Column(String(20), default=HabitType.BOOLEAN)
    frequency = Column(String(20), default=HabitFrequency.DAILY)
    target_value = Column(Float, default=1.0)  # Target count/duration
    unit = Column(String(50), nullable=True)  # e.g., "minutes", "reps", "pages"
    
    # Visual customization
    icon = Column(String(100), default="🎯")
    color = Column(String(7), default="#3B82F6")  # Hex color
    
    # Settings
    is_active = Column(Boolean, default=True)
    reminder_enabled = Column(Boolean, default=False)
    reminder_time = Column(String(5), nullable=True)  # HH:MM format
    
    # Tracking
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    total_completions = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="habits")
    entries = relationship("HabitEntry", back_populates="habit", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Habit(id={self.id}, name='{self.name}', owner_id={self.owner_id})>"

