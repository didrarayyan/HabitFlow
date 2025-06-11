"""
Database configuration and connection setup.
Handles SQLAlchemy engine, session, and table creation.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings


# Create database engine
if settings.USE_SQLITE:
    engine = create_engine(
        settings.SQLITE_DATABASE_URI,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(
        str(settings.SQLALCHEMY_DATABASE_URI),
        pool_pre_ping=True,
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_tables():
    """Create all database tables."""
    # Import all models to ensure they are registered
    from app.models import user, habit, habit_entry  # noqa
    
    Base.metadata.create_all(bind=engine)

