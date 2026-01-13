from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
from enum import Enum
from ..database import Base


class RemarkStatus(str, Enum):
    """Перечисление статусов замечаний"""
    NEW = "new"           # Новое замечание
    IN_PROGRESS = "in_progress"  # В работе
    FIXED = "fixed"       # Исправлено
    VERIFIED = "verified"  # Проверено
    CLOSED = "closed"     # Закрыто
    REJECTED = "rejected"  # Отклонено


class ConstructionRemark(Base):
    """
    Модель для хранения замечаний от строительного контроля
    """
    __tablename__ = "construction_remarks"

    id = Column(Integer, primary_key=True, index=True)
    remark_number = Column(String, unique=True, index=True, nullable=False)  # Номер замечания
    project_object_id = Column(Integer, ForeignKey("project_objects.id"), index=True, nullable=False)  # Объект проекта
    title = Column(String, index=True, nullable=False)  # Заголовок замечания
    description = Column(Text, nullable=False)  # Описание замечания
    status = Column(SQLEnum(RemarkStatus), default=RemarkStatus.NEW, index=True)  # Статус замечания
    priority = Column(String, default="normal", index=True)  # Приоритет: low, normal, high, critical
    assigned_to = Column(String, index=True, nullable=True)  # Кому назначено
    deadline = Column(DateTime, nullable=True)  # Срок исправления
    created_by = Column(String, index=True, nullable=False)  # Кто создал
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    project_object = relationship("ProjectObject", back_populates="remarks")
    photos = relationship("RemarkPhoto", back_populates="remark")
    history = relationship("RemarkHistory", back_populates="remark")


class RemarkPhoto(Base):
    """
    Модель для хранения фотографий к замечаниям
    """
    __tablename__ = "remark_photos"

    id = Column(Integer, primary_key=True, index=True)
    remark_id = Column(Integer, ForeignKey("construction_remarks.id"), index=True, nullable=False)  # Ссылка на замечание
    file_path = Column(String, nullable=False)  # Путь к файлу на сервере
    filename = Column(String, nullable=False)  # Имя файла
    file_size = Column(Integer, nullable=False)  # Размер файла в байтах
    description = Column(Text, nullable=True)  # Описание фотографии
    created_by = Column(String, index=True, nullable=False)  # Кто загрузил
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    remark = relationship("ConstructionRemark", back_populates="photos")


class RemarkHistory(Base):
    """
    Модель для хранения истории изменений статуса замечаний
    """
    __tablename__ = "remark_history"

    id = Column(Integer, primary_key=True, index=True)
    remark_id = Column(Integer, ForeignKey("construction_remarks.id"), index=True, nullable=False)  # Ссылка на замечание
    old_status = Column(SQLEnum(RemarkStatus), nullable=True)  # Предыдущий статус
    new_status = Column(SQLEnum(RemarkStatus), nullable=False)  # Новый статус
    comment = Column(Text, nullable=True)  # Комментарий к изменению
    changed_by = Column(String, index=True, nullable=False)  # Кто изменил
    changed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    remark = relationship("ConstructionRemark", back_populates="history")


# Добавим связь к модели ProjectObject
def add_remarks_relationship():
    from .gpr import ProjectObject
    ProjectObject.remarks = relationship("ConstructionRemark", back_populates="project_object")