"""
Habit entry model for tracking daily habit completions.
"""

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import date

from app.core.database import Base


class HabitEntry(Base):
    """Habit entry model for tracking daily completions."""
    
    __tablename__ = "habit_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Entry data
    date = Column(Date, nullable=False, default=date.today)
    completed = Column(Boolean, default=False)
    value = Column(Float, nullable=True)  # Actual count/duration achieved
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    habit = relationship("Habit", back_populates="entries")
    user = relationship("User", back_populates="habit_entries")
    
    # Unique constraint to prevent duplicate entries for same habit on same date
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )
    
    def __repr__(self):
        return f"<HabitEntry(id={self.id}, habit_id={self.habit_id}, date={self.date}, completed={self.completed})>"

