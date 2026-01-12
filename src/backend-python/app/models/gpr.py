from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Dict, Any
from ..database import Base


class Customer(Base):
    """
    Модель для хранения информации о заказчиках
    """
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, unique=True, index=True, nullable=False)  # Уникальный ID заказчика
    name = Column(String, nullable=False)  # Название заказчика
    contact_info = Column(String, nullable=True)  # Контактная информация
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    gpr_records = relationship("GPRRecord", back_populates="customer")


class ProjectObject(Base):
    """
    Модель для хранения информации об объектах проекта
    """
    __tablename__ = "project_objects"

    id = Column(Integer, primary_key=True, index=True)
    object_id = Column(String, unique=True, index=True, nullable=False)  # Уникальный ID объекта
    name = Column(String, nullable=False)  # Название объекта
    location = Column(String, nullable=True)  # Местоположение объекта
    description = Column(String, nullable=True)  # Описание объекта
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    gpr_records = relationship("GPRRecord", back_populates="project_object")


class GPRRecord(Base):
    """
    Модель для хранения записей Графика Производства Работ (ГПР)
    """
    __tablename__ = "gpr_records"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), index=True, nullable=False)  # Связь с заказчиком
    object_id = Column(Integer, ForeignKey("project_objects.id"), index=True, nullable=False)  # Связь с объектом
    work_type = Column(String, index=True, nullable=False)   # Тип работ (материал исполнения)
    volume_plan = Column(Float, nullable=False)  # Объем планируемых работ
    volume_fact = Column(Float, default=0.0)     # Объем фактически выполненных работ
    volume_remainder = Column(Float, default=0.0) # Остаток объема
    progress = Column(Float, default=0.0, index=True)        # Процент выполнения
    daily_data = Column(String, default="{}")    # JSON строка с ежедневными данными
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    customer = relationship("Customer", back_populates="gpr_records")
    project_object = relationship("ProjectObject", back_populates="gpr_records")


class WeeklyReport(Base):
    """
    Модель для хранения недельных отчетов
    """
    __tablename__ = "weekly_reports"

    id = Column(Integer, primary_key=True, index=True)
    week_start_date = Column(DateTime, index=True, nullable=False)  # Дата начала недели
    report_data = Column(String, nullable=False)        # JSON строка с данными отчета
    created_by = Column(String, index=True, nullable=False)         # Кто сформировал отчет
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Material(Base):
    """
    Модель для справочника материалов
    """
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)  # Название материала
    description = Column(String, index=True, nullable=True)                    # Описание материала
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# Добавим справочник материалов в базу данных
MATERIALS_REFERENCE = [
    {"id": "kraska_b", "name": "Краска б"},
    {"id": "kraska_ch", "name": "Краска ч"},
    {"id": "vremyanka", "name": "Времянка"},
    {"id": "kraska_j", "name": "Краска ж"},
    {"id": "hp", "name": "ХП"},
    {"id": "hpj", "name": "ХПж"},
    {"id": "tp", "name": "ТП"},
    {"id": "demarkirovka", "name": "Демаркировка"}
]

# Добавим связи к модели Material
Material.requests = relationship("MaterialRequest", back_populates="material")
Material.stocks = relationship("MaterialStock", back_populates="material")