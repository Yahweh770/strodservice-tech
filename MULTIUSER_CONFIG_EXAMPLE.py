"""
Пример конфигурационного файла для поддержки многопользовательского режима
в приложении "Строд-Сервис Технолоджи"
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import timedelta

# Конфигурация базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./strod_service_tech.db")

# Определяем тип базы данных и настраиваем соответствующий движок
if "postgresql" in DATABASE_URL.lower():
    # Настройки для PostgreSQL в многопользовательской среде
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,  # Размер пула соединений для поддержки нескольких пользователей
        max_overflow=30,  # Максимальное количество дополнительных соединений
        pool_pre_ping=True,  # Проверка соединения перед использованием
        pool_recycle=300,  # Пересоздание соединений каждые 5 минут
        echo=False  # Включение логирования SQL-запросов (только для отладки)
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
    # Для SQLite (однопользовательский режим, в основном для разработки)
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Разрешить доступ из разных потоков
        echo=False
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Конфигурация безопасности
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Настройки многопользовательской среды
MAX_CONCURRENT_USERS = int(os.getenv("MAX_CONCURRENT_USERS", "50"))  # Максимальное количество одновременных пользователей
SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "120"))  # Таймаут сессии в минутах
ENABLE_REALTIME_SYNC = os.getenv("ENABLE_REALTIME_SYNC", "True").lower() == "true"  # Включить синхронизацию в реальном времени

# Настройки кэширования для повышения производительности в многопользовательской среде
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "300"))  # Время жизни кэша в секундах
USE_REDIS_CACHE = os.getenv("USE_REDIS_CACHE", "False").lower() == "true"  # Использовать Redis для кэширования
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Настройки логирования аудита для отслеживания действий пользователей
AUDIT_LOG_ENABLED = os.getenv("AUDIT_LOG_ENABLED", "True").lower() == "true"
AUDIT_LOG_LEVEL = os.getenv("AUDIT_LOG_LEVEL", "INFO")  # INFO, DEBUG, WARNING, ERROR

# Настройки уведомлений для командной работы
NOTIFICATIONS_ENABLED = os.getenv("NOTIFICATIONS_ENABLED", "True").lower() == "true"
EMAIL_NOTIFICATIONS_ENABLED = os.getenv("EMAIL_NOTIFICATIONS_ENABLED", "False").lower() == "true"
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# Настройки файлового хранилища для совместной работы с документами
FILE_STORAGE_TYPE = os.getenv("FILE_STORAGE_TYPE", "local")  # local, s3, azure
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))  # Максимальный размер файла в МБ
ALLOWED_FILE_EXTENSIONS = os.getenv("ALLOWED_FILE_EXTENSIONS", "pdf,doc,docx,xlsx,jpg,png").split(",")

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Создание токена доступа с учетом настроек безопасности"""
    from datetime import datetime
    from jose import jwt
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_active_user_config():
    """Получение конфигурации для проверки активного пользователя"""
    return {
        "require_active_session": True,
        "check_permissions": True,
        "audit_user_actions": AUDIT_LOG_ENABLED
    }

# Вывод основных настроек при запуске
print("Конфигурация многопользовательского режима загружена:")
print(f"- Поддержка до {MAX_CONCURRENT_USERS} одновременных пользователей")
print(f"- Время сессии: {SESSION_TIMEOUT_MINUTES} минут")
print(f"- База данных: {DATABASE_URL.split('://')[0] if '://' in DATABASE_URL else 'sqlite'}")
print(f"- Включена синхронизация в реальном времени: {ENABLE_REALTIME_SYNC}")
print(f"- Кэширование: {'Redis' if USE_REDIS_CACHE else 'локальное'} ({CACHE_TTL_SECONDS} сек)")