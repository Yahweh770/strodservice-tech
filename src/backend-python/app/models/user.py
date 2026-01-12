from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional
from ..database import Base


class User(Base):
    """
    Модель пользователя для аутентификации
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)  # Логин пользователя
    email = Column(String, unique=True, index=True, nullable=True)     # Email пользователя
    hashed_password = Column(String, nullable=False)                   # Хэш пароля
    full_name = Column(String, nullable=True)                          # Полное имя
    position = Column(String, nullable=True)                           # Должность
    department = Column(String, nullable=True)                         # Отдел
    is_active = Column(Boolean, default=True, index=True)              # Активен ли пользователь
    is_admin = Column(Boolean, default=False, index=True)              # Является ли администратором
    permissions = Column(String, default="{}")                         # JSON строка с правами доступа
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    documents_created = relationship("UploadedFile", back_populates="uploader")
    material_requests = relationship("MaterialRequest", back_populates="requester")


class UserSession(Base):
    """
    Модель для хранения сессий пользователей
    """
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_token = Column(String, unique=True, index=True, nullable=False)  # Токен сессии
    expires_at = Column(DateTime, nullable=False)                             # Время истечения
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    user = relationship("User")