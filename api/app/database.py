from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from functools import lru_cache
import os

from .config import get_settings

# Base class for ORM models
Base = declarative_base()

# Global variables for lazy initialization
_engine = None
_SessionLocal = None


def get_database_url() -> str:
    """
    Returns the appropriate database URL based on environment.
    In production (Cloud Run), uses Cloud SQL connector.
    In development, uses standard PostgreSQL connection string.
    """
    settings = get_settings()
    if settings.app_env == "production" and settings.cloud_sql_connection_name:
        # For Cloud Run with Cloud SQL, we use pg8000 with Cloud SQL connector
        return f"postgresql+pg8000://{settings.db_user}:{settings.db_password}@/{settings.db_name}"
    return settings.database_url


def create_cloud_sql_engine():
    """
    Creates SQLAlchemy engine with Cloud SQL connector for production.
    """
    from google.cloud.sql.connector import Connector
    
    settings = get_settings()
    connector = Connector()
    
    def getconn():
        return connector.connect(
            settings.cloud_sql_connection_name,
            "pg8000",
            user=settings.db_user,
            password=settings.db_password,
            db=settings.db_name,
        )
    
    return create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,
    )


def get_engine():
    """Returns the appropriate engine based on environment. Lazily initialized."""
    global _engine
    if _engine is None:
        settings = get_settings()
        if settings.app_env == "production" and settings.cloud_sql_connection_name:
            _engine = create_cloud_sql_engine()
        else:
            _engine = create_engine(
                settings.database_url,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=2,
                pool_timeout=30,
                pool_recycle=1800,
            )
    return _engine


def get_session_local():
    """Returns SessionLocal factory. Lazily initialized."""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal


def get_db():
    """
    Dependency that provides a database session.
    Yields a database session and ensures it's closed after use.
    """
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=get_engine())
