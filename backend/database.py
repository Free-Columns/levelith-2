"""
Database Configuration and Session Management

Provides SQLAlchemy engine, session management, and base model.
Supports both sync and async database operations.
"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, event, Engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from backend.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,  # Verify connections before using
    echo=settings.debug,  # Log SQL in debug mode
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Set SQLite pragmas if using SQLite (for local development)."""
    if "sqlite" in settings.database_url:
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting database session.

    Usage:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()

    Yields:
        Database session that is automatically closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Context manager for database session.

    Usage:
        with get_db_context() as db:
            user = db.query(User).first()

    Yields:
        Database session that is automatically closed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database by creating all tables.

    Should be called on application startup.
    Creates all tables defined in models that inherit from Base.

    Retries connection with exponential backoff if database is temporarily unavailable.
    """
    import logging
    import time

    logger = logging.getLogger(__name__)

    # Import all models here to ensure they are registered with Base
    from backend.models import user, experience  # noqa: F401
    from backend.models.db_models import NAICSCodeDB  # noqa: F401

    max_retries = 5
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to initialize database (attempt {attempt + 1}/{max_retries})...")
            Base.metadata.create_all(bind=engine)
            logger.info("Database initialized successfully")
            return
        except Exception as e:
            logger.warning(f"Database initialization attempt {attempt + 1} failed: {e}")

            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logger.error("Failed to initialize database after all retries")
                # Don't crash the app - just log the error
                # The health check endpoint will show database is unhealthy
                logger.warning("Application will start without database connection")
                logger.warning("Database endpoints will fail until connection is established")


def drop_db() -> None:
    """
    Drop all database tables.

    WARNING: This will destroy all data!
    Should only be used in development/testing.
    """
    if settings.is_production:
        raise RuntimeError("Cannot drop database in production!")

    Base.metadata.drop_all(bind=engine)


def reset_db() -> None:
    """
    Reset database by dropping and recreating all tables.

    WARNING: This will destroy all data!
    Should only be used in development/testing.
    """
    if settings.is_production:
        raise RuntimeError("Cannot reset database in production!")

    drop_db()
    init_db()


class DatabaseHealthCheck:
    """Database health check utility."""

    @staticmethod
    def check() -> bool:
        """
        Check if database connection is healthy.

        Returns:
            True if database is accessible, False otherwise.
        """
        try:
            with get_db_context() as db:
                db.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    @staticmethod
    def get_info() -> dict:
        """
        Get database connection information.

        Returns:
            Dictionary with database status information.
        """
        try:
            with get_db_context() as db:
                # Use database-agnostic query for version info
                # PostgreSQL: version(), SQLite: sqlite_version()
                if "postgresql" in settings.database_url:
                    result = db.execute(text("SELECT version()"))
                    version = result.scalar()
                elif "sqlite" in settings.database_url:
                    result = db.execute(text("SELECT sqlite_version()"))
                    version = f"SQLite {result.scalar()}"
                else:
                    version = "unknown"

                return {
                    "status": "healthy",
                    "database": settings.database_url.split("@")[-1] if "@" in settings.database_url else "unknown",
                    "version": version,
                    "pool_size": settings.database_pool_size,
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
