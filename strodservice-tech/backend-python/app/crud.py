from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from . import models, schemas


def get_gpr_records(db: Session, skip: int = 0, limit: int = 100):
    """Получить список записей ГПР"""
    return db.query(models.GPRRecord).offset(skip).limit(limit).all()


def get_gpr_record(db: Session, record_id: int):
    """Получить запись ГПР по ID"""
    return db.query(models.GPRRecord).filter(models.GPRRecord.id == record_id).first()


def get_weekly_report_by_date(db: Session, week_start_date: datetime.date):
    """Получить недельный отчет по дате начала недели"""
    from sqlalchemy import cast, Date
    return db.query(models.WeeklyReport).filter(
        cast(models.WeeklyReport.week_start_date, Date) == week_start_date
    ).first()


def get_materials(db: Session, skip: int = 0, limit: int = 100):
    """Получить список материалов"""
    return db.query(models.Material).offset(skip).limit(limit).all()


def get_material(db: Session, material_id: int):
    """Получить материал по ID"""
    return db.query(models.Material).filter(models.Material.id == material_id).first()


def create_material(db: Session, material: schemas.MaterialCreate):
    """Создать новый материал"""
    db_material = models.Material(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


def update_material(db: Session, material_id: int, material_update: schemas.MaterialUpdate):
    """Обновить материал"""
    db_material = get_material(db, material_id)
    if db_material:
        update_data = material_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_material, field, value)
        db.commit()
        db.refresh(db_material)
    return db_material


def delete_material(db: Session, material_id: int):
    """Удалить материал"""
    db_material = get_material(db, material_id)
    if db_material:
        db.delete(db_material)
        db.commit()
    return db_material