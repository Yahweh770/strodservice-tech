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


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    """Получить список заказчиков"""
    return db.query(models.Customer).offset(skip).limit(limit).all()


def get_customer(db: Session, customer_id: int):
    """Получить заказчика по ID"""
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customer_by_customer_id(db: Session, customer_id: str):
    """Получить заказчика по customer_id"""
    return db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()


def create_customer(db: Session, customer: schemas.CustomerCreate):
    """Создать нового заказчика"""
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update_customer(db: Session, customer_id: int, customer_update: schemas.CustomerUpdate):
    """Обновить заказчика"""
    db_customer = get_customer(db, customer_id)
    if db_customer:
        update_data = customer_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int):
    """Удалить заказчика"""
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer


def get_project_objects(db: Session, skip: int = 0, limit: int = 100):
    """Получить список объектов проекта"""
    return db.query(models.ProjectObject).offset(skip).limit(limit).all()


def get_project_object(db: Session, object_id: int):
    """Получить объект проекта по ID"""
    return db.query(models.ProjectObject).filter(models.ProjectObject.id == object_id).first()


def get_project_object_by_object_id(db: Session, object_id: str):
    """Получить объект проекта по object_id"""
    return db.query(models.ProjectObject).filter(models.ProjectObject.object_id == object_id).first()


def create_project_object(db: Session, project_object: schemas.ProjectObjectCreate):
    """Создать новый объект проекта"""
    db_project_object = models.ProjectObject(**project_object.dict())
    db.add(db_project_object)
    db.commit()
    db.refresh(db_project_object)
    return db_project_object


def update_project_object(db: Session, object_id: int, project_object_update: schemas.ProjectObjectUpdate):
    """Обновить объект проекта"""
    db_project_object = get_project_object(db, object_id)
    if db_project_object:
        update_data = project_object_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project_object, field, value)
        db.commit()
        db.refresh(db_project_object)
    return db_project_object


def delete_project_object(db: Session, object_id: int):
    """Удалить объект проекта"""
    db_project_object = get_project_object(db, object_id)
    if db_project_object:
        db.delete(db_project_object)
        db.commit()
    return db_project_object