from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Dict, Any
from ..database import Base


class GPRRecord(Base):
    """
    Модель для хранения записей Графика Производства Работ (ГПР)
    """
    __tablename__ = "gpr_records"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, nullable=False)  # ID заказчика из связанной таблицы
    object_id = Column(String, nullable=False)    # ID объекта из связанной таблицы
    work_type = Column(String, nullable=False)   # Тип работ (материал исполнения)
    volume_plan = Column(Float, nullable=False)  # Объем планируемых работ
    volume_fact = Column(Float, default=0.0)     # Объем фактически выполненных работ
    volume_remainder = Column(Float, default=0.0) # Остаток объема
    progress = Column(Float, default=0.0)        # Процент выполнения
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
    week_start_date = Column(DateTime, nullable=False)  # Дата начала недели
    report_data = Column(String, nullable=False)        # JSON строка с данными отчета
    created_by = Column(String, nullable=False)         # Кто сформировал отчет
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Material(Base):
    """
    Модель для справочника материалов
    """
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)  # Название материала
    description = Column(String, nullable=True)                    # Описание материала
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    gpr_records = relationship("GPRRecord", back_populates="material")


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