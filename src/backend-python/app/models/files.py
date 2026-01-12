from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
from ..database import Base


class FileCategory(Base):
    """
    Модель для категорий файлов
    """
    __tablename__ = "file_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)  # Название категории
    description = Column(Text, nullable=True)                       # Описание категории
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UploadedFile(Base):
    """
    Модель для загруженных файлов
    """
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True, nullable=False)              # Оригинальное имя файла
    original_filename = Column(String, index=True, nullable=False)     # Оригинальное имя файла от пользователя
    file_path = Column(String, nullable=False)             # Путь к файлу на сервере
    file_size = Column(Integer, nullable=False)            # Размер файла в байтах
    content_type = Column(String, nullable=True)           # MIME тип файла
    category_id = Column(Integer, ForeignKey("file_categories.id"), index=True, nullable=True)  # Категория файла
    section_id = Column(String, index=True, nullable=True)             # ID секции, с которой связан файл
    section_name = Column(String, index=True, nullable=True)           # Название секции
    project_id = Column(String, index=True, nullable=True)             # ID проекта
    uploaded_by = Column(String, index=True, nullable=False)           # Кто загрузил файл
    uploader_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)  # ID пользователя, который загрузил файл
    description = Column(Text, nullable=True)              # Описание файла
    is_active = Column(Boolean, default=True, index=True)              # Активен ли файл
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    category = relationship("FileCategory", back_populates="files")
    uploader = relationship("User", back_populates="documents_created")


class MaterialRequest(Base):
    """
    Модель для запросов на закупку материалов
    """
    __tablename__ = "material_requests"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), index=True, nullable=False)  # ID материала
    requested_quantity = Column(Integer, nullable=False)      # Запрашиваемое количество
    available_quantity = Column(Integer, default=0)           # Доступное количество
    needed_quantity = Column(Integer, nullable=False)         # Необходимое количество
    section_id = Column(String, index=True, nullable=True)                # ID секции, где требуется материал
    section_name = Column(String, index=True, nullable=True)              # Название секции
    project_id = Column(String, index=True, nullable=True)                # ID проекта
    reason = Column(Text, nullable=True)                      # Причина запроса
    status = Column(String, index=True, default="pending")                # Статус запроса: pending, approved, rejected, fulfilled
    requested_by = Column(String, index=True, nullable=False)             # Кто запросил
    requester_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)  # ID пользователя, который запросил
    approved_by = Column(String, index=True, nullable=True)               # Кто одобрил
    approved_at = Column(DateTime(timezone=True), nullable=True)  # Когда одобрен
    fulfilled_at = Column(DateTime(timezone=True), nullable=True)  # Когда выполнен
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    material = relationship("Material", back_populates="requests")
    requester = relationship("User", back_populates="material_requests")


class MaterialStock(Base):
    """
    Модель для учета остатков материалов
    """
    __tablename__ = "material_stocks"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), index=True, nullable=False)  # ID материала
    quantity = Column(Integer, default=0)                     # Количество на складе
    reserved_quantity = Column(Integer, default=0)            # Зарезервированное количество
    min_threshold = Column(Integer, default=10)               # Минимальный порог для уведомления
    location = Column(String, index=True, nullable=True)                  # Местоположение склада
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    material = relationship("Material", back_populates="stock")


# Add back_populates to the Material model relationships
FileCategory.files = relationship("UploadedFile", back_populates="category")
Material.requests = relationship("MaterialRequest", back_populates="material")
Material.stocks = relationship("MaterialStock", back_populates="material")