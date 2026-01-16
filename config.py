"""
Unified configuration for the StrodService project supporting multi-user mode
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import timedelta


class Config:
    """Base configuration class"""
    
    # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./strod_service_main.db")
    
    # Determine database type and configure accordingly
    if "postgresql" in DATABASE_URL.lower():
        # PostgreSQL settings for multi-user environment
        engine = create_engine(
            DATABASE_URL,
            pool_size=20,  # Connection pool size for multi-user support
            max_overflow=30,  # Maximum additional connections
            pool_pre_ping=True,  # Check connection before use
            pool_recycle=300,  # Recreate connections every 5 minutes
            echo=False  # Enable SQL logging only for debugging
        )
    elif "mysql" in DATABASE_URL.lower():
        engine = create_engine(
            DATABASE_URL,
            pool_size=15,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False
        )
    else:
        # For SQLite (single-user mode, mainly for development)
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},  # Allow access from different threads
            echo=False
        )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    # Security configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Multi-user environment settings
    MAX_CONCURRENT_USERS = int(os.getenv("MAX_CONCURRENT_USERS", "50"))  # Max concurrent users
    SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "120"))  # Session timeout in minutes
    ENABLE_REALTIME_SYNC = os.getenv("ENABLE_REALTIME_SYNC", "True").lower() == "true"  # Enable real-time sync
    MULTI_USER_MODE = os.getenv("MULTI_USER_MODE", "False").lower() == "true"  # Enable multi-user mode

    # Caching settings for performance in multi-user environment
    CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "300"))  # Cache TTL in seconds
    USE_REDIS_CACHE = os.getenv("USE_REDIS_CACHE", "False").lower() == "true"  # Use Redis for caching
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Audit logging settings for tracking user actions
    AUDIT_LOG_ENABLED = os.getenv("AUDIT_LOG_ENABLED", "True").lower() == "true"
    AUDIT_LOG_LEVEL = os.getenv("AUDIT_LOG_LEVEL", "INFO")  # INFO, DEBUG, WARNING, ERROR

    # Notification settings for team collaboration
    NOTIFICATIONS_ENABLED = os.getenv("NOTIFICATIONS_ENABLED", "True").lower() == "true"
    EMAIL_NOTIFICATIONS_ENABLED = os.getenv("EMAIL_NOTIFICATIONS_ENABLED", "False").lower() == "true"
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

    # File storage settings for collaborative document work
    FILE_STORAGE_TYPE = os.getenv("FILE_STORAGE_TYPE", "local")  # local, s3, azure
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))  # Max file size in MB
    ALLOWED_FILE_EXTENSIONS = os.getenv("ALLOWED_FILE_EXTENSIONS", "pdf,doc,docx,xlsx,jpg,png").split(",")


# Create config instance
config = Config()


def get_db():
    """Dependency for getting database session"""
    db = config.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create access token with security settings"""
    from datetime import datetime
    from jose import jwt
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def get_current_active_user_config():
    """Get configuration for checking active user"""
    return {
        "require_active_session": True,
        "check_permissions": True,
        "audit_user_actions": config.AUDIT_LOG_ENABLED
    }


# Print basic settings on startup
print("Multi-user mode configuration loaded:")
print(f"- Support up to {config.MAX_CONCURRENT_USERS} concurrent users")
print(f"- Session timeout: {config.SESSION_TIMEOUT_MINUTES} minutes")
print(f"- Database: {config.DATABASE_URL.split('://')[0] if '://' in config.DATABASE_URL else 'sqlite'}")
print(f"- Real-time sync enabled: {config.ENABLE_REALTIME_SYNC}")
print(f"- Caching: {'Redis' if config.USE_REDIS_CACHE else 'local'} ({config.CACHE_TTL_SECONDS} sec)")
print(f"- Multi-user mode: {config.MULTI_USER_MODE}")