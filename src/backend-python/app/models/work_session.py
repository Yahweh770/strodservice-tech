from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional
from ..database import Base


class WorkSession(Base):
    """
    Модель для отслеживания сессий работы сотрудников
    """
    __tablename__ = "work_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)  # Время начала работы
    end_time = Column(DateTime(timezone=True), nullable=True)    # Время окончания работы
    is_active = Column(Boolean, default=True, index=True)        # Активна ли сессия
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    user = relationship("User")