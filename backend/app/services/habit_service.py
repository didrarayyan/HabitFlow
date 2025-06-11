"""
Habit service for habit management operations.
"""

from typing import Any, Dict, List, Optional, Union
from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.models.habit import Habit
from app.models.habit_entry import HabitEntry
from app.schemas.habit import HabitCreate, HabitUpdate, HabitEntryCreate, HabitEntryUpdate


class HabitService:
    """Habit service for database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, id: int) -> Optional[Habit]:
        """Get habit by ID."""
        return self.db.query(Habit).filter(Habit.id == id).first()
    
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Habit]:
        """Get habits by user ID."""
        return (
            self.db.query(Habit)
            .filter(Habit.owner_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_active_by_user(self, user_id: int) -> List[Habit]:
        """Get active habits by user ID."""
        return (
            self.db.query(Habit)
            .filter(and_(Habit.owner_id == user_id, Habit.is_active == True))
            .all()
        )
    
    def create(self, *, obj_in: HabitCreate, user_id: int) -> Habit:
        """Create new habit."""
        db_obj = Habit(
            **obj_in.dict(),
            owner_id=user_id,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        *,
        db_obj: Habit,
        obj_in: Union[HabitUpdate, Dict[str, Any]]
    ) -> Habit:
        """Update habit."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, *, id: int) -> Habit:
        """Delete habit."""
        obj = self.db.query(Habit).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj
    
    def update_streak(self, habit: Habit) -> Habit:
        """Update habit streak based on recent entries."""
        # Get recent entries ordered by date descending
        recent_entries = (
            self.db.query(HabitEntry)
            .filter(HabitEntry.habit_id == habit.id)
            .order_by(HabitEntry.date.desc())
            .limit(30)
            .all()
        )
        
        if not recent_entries:
            habit.current_streak = 0
            self.db.commit()
            return habit
        
        # Calculate current streak
        current_streak = 0
        today = date.today()
        
        for entry in recent_entries:
            if entry.completed:
                if entry.date == today or entry.date == today - timedelta(days=current_streak):
                    current_streak += 1
                else:
                    break
            else:
                break
        
        habit.current_streak = current_streak
        
        # Update longest streak if current is longer
        if current_streak > habit.longest_streak:
            habit.longest_streak = current_streak
        
        self.db.commit()
        return habit


class HabitEntryService:
    """Habit entry service for database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, id: int) -> Optional[HabitEntry]:
        """Get habit entry by ID."""
        return self.db.query(HabitEntry).filter(HabitEntry.id == id).first()
    
    def get_by_habit_and_date(self, habit_id: int, entry_date: date) -> Optional[HabitEntry]:
        """Get habit entry by habit ID and date."""
        return (
            self.db.query(HabitEntry)
            .filter(and_(HabitEntry.habit_id == habit_id, HabitEntry.date == entry_date))
            .first()
        )
    
    def get_by_habit(self, habit_id: int, skip: int = 0, limit: int = 100) -> List[HabitEntry]:
        """Get habit entries by habit ID."""
        return (
            self.db.query(HabitEntry)
            .filter(HabitEntry.habit_id == habit_id)
            .order_by(HabitEntry.date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_user_and_date(self, user_id: int, entry_date: date) -> List[HabitEntry]:
        """Get habit entries by user ID and date."""
        return (
            self.db.query(HabitEntry)
            .filter(and_(HabitEntry.user_id == user_id, HabitEntry.date == entry_date))
            .all()
        )
    
    def create(self, *, obj_in: HabitEntryCreate, user_id: int) -> HabitEntry:
        """Create new habit entry."""
        # Check if entry already exists for this habit and date
        existing = self.get_by_habit_and_date(obj_in.habit_id, obj_in.date)
        if existing:
            # Update existing entry instead
            return self.update(db_obj=existing, obj_in=obj_in.dict())
        
        db_obj = HabitEntry(
            **obj_in.dict(),
            user_id=user_id,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        
        # Update habit statistics
        habit = self.db.query(Habit).filter(Habit.id == obj_in.habit_id).first()
        if habit and db_obj.completed:
            habit.total_completions += 1
            self.db.commit()
        
        return db_obj
    
    def update(
        self,
        *,
        db_obj: HabitEntry,
        obj_in: Union[HabitEntryUpdate, Dict[str, Any]]
    ) -> HabitEntry:
        """Update habit entry."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        # Track completion change for statistics
        was_completed = db_obj.completed
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        
        # Update habit statistics if completion status changed
        if "completed" in update_data:
            habit = self.db.query(Habit).filter(Habit.id == db_obj.habit_id).first()
            if habit:
                if db_obj.completed and not was_completed:
                    habit.total_completions += 1
                elif not db_obj.completed and was_completed:
                    habit.total_completions = max(0, habit.total_completions - 1)
                self.db.commit()
        
        return db_obj
    
    def delete(self, *, id: int) -> HabitEntry:
        """Delete habit entry."""
        obj = self.db.query(HabitEntry).get(id)
        
        # Update habit statistics if entry was completed
        if obj and obj.completed:
            habit = self.db.query(Habit).filter(Habit.id == obj.habit_id).first()
            if habit:
                habit.total_completions = max(0, habit.total_completions - 1)
                self.db.commit()
        
        self.db.delete(obj)
        self.db.commit()
        return obj

