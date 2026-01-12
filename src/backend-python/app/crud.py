from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
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


# CRUD операции для типов документов
def get_document_type(db: Session, document_type_id: int):
    return db.query(models.DocumentType).filter(models.DocumentType.id == document_type_id).first()


def get_document_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DocumentType).offset(skip).limit(limit).all()


def create_document_type(db: Session, document_type: schemas.DocumentTypeCreate):
    db_document_type = models.DocumentType(**document_type.model_dump())
    db.add(db_document_type)
    db.commit()
    db.refresh(db_document_type)
    return db_document_type


def update_document_type(db: Session, document_type_id: int, document_type: schemas.DocumentTypeCreate):
    db_document_type = get_document_type(db, document_type_id)
    if db_document_type:
        for key, value in document_type.model_dump().items():
            setattr(db_document_type, key, value)
        db.commit()
        db.refresh(db_document_type)
    return db_document_type


def delete_document_type(db: Session, document_type_id: int):
    db_document_type = get_document_type(db, document_type_id)
    if db_document_type:
        db.delete(db_document_type)
        db.commit()
    return db_document_type


# CRUD операции для документов
def get_document(db: Session, document_id: int):
    return db.query(models.Document).filter(models.Document.id == document_id).first()


def get_documents(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    project_id: Optional[str] = None, 
    status: Optional[str] = None,
    doc_number: Optional[str] = None,
    title: Optional[str] = None
):
    query = db.query(models.Document)
    
    if project_id:
        query = query.filter(models.Document.project_id == project_id)
    if status:
        query = query.filter(models.Document.status == status)
    if doc_number:
        query = query.filter(models.Document.doc_number.contains(doc_number))
    if title:
        query = query.filter(models.Document.title.contains(title))
        
    return query.offset(skip).limit(limit).all()


def create_document(db: Session, document: schemas.DocumentCreate):
    db_document = models.Document(**document.model_dump(), status="in_office")
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def update_document(db: Session, document_id: int, document: schemas.DocumentUpdate):
    db_document = get_document(db, document_id)
    if db_document:
        for key, value in document.model_dump(exclude_unset=True).items():
            setattr(db_document, key, value)
        db.commit()
        db.refresh(db_document)
    return db_document


def delete_document(db: Session, document_id: int):
    db_document = get_document(db, document_id)
    if db_document:
        db.delete(db_document)
        db.commit()
    return db_document


def search_documents(
    db: Session, 
    query_str: Optional[str] = None, 
    project_id: Optional[str] = None, 
    status: Optional[str] = None
):
    """Поиск документов по различным критериям"""
    db_query = db.query(models.Document)
    
    if query_str:
        # Поиск по номеру документа или названию
        db_query = db_query.filter(
            or_(
                models.Document.doc_number.contains(query_str),
                models.Document.title.contains(query_str)
            )
        )
    
    if project_id:
        db_query = db_query.filter(models.Document.project_id == project_id)
    
    if status:
        db_query = db_query.filter(models.Document.status == status)
    
    return db_query.all()


# CRUD операции для отправок документов
def get_document_shipment(db: Session, shipment_id: int):
    return db.query(models.DocumentShipment).filter(models.DocumentShipment.id == shipment_id).first()


def get_document_shipments(db: Session, document_id: int):
    return db.query(models.DocumentShipment).filter(models.DocumentShipment.document_id == document_id).all()


def create_document_shipment(db: Session, shipment: schemas.DocumentShipmentCreate):
    db_shipment = models.DocumentShipment(**shipment.model_dump())
    db.add(db_shipment)
    
    # Обновляем статус документа на "отправлен"
    document = get_document(db, shipment.document_id)
    if document:
        document.status = "shipped"
        document.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_shipment)
    return db_shipment


def update_document_shipment(db: Session, shipment_id: int, shipment: schemas.DocumentShipmentUpdate):
    db_shipment = get_document_shipment(db, shipment_id)
    if db_shipment:
        for key, value in shipment.model_dump(exclude_unset=True).items():
            setattr(db_shipment, key, value)
        db.commit()
        db.refresh(db_shipment)
    return db_shipment


def delete_document_shipment(db: Session, shipment_id: int):
    db_shipment = get_document_shipment(db, shipment_id)
    if db_shipment:
        db.delete(db_shipment)
        db.commit()
    return db_shipment


# CRUD операции для возвратов документов
def get_document_return(db: Session, return_id: int):
    return db.query(models.DocumentReturn).filter(models.DocumentReturn.id == return_id).first()


def get_document_returns(db: Session, document_id: int):
    return db.query(models.DocumentReturn).filter(models.DocumentReturn.document_id == document_id).all()


def create_document_return(db: Session, return_obj: schemas.DocumentReturnCreate):
    db_return = models.DocumentReturn(**return_obj.model_dump())
    db.add(db_return)
    
    # Обновляем статус документа на "возвращен"
    document = get_document(db, return_obj.document_id)
    if document:
        document.status = "returned"
        document.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_return)
    return db_return


def update_document_return(db: Session, return_id: int, return_obj: schemas.DocumentReturnUpdate):
    db_return = get_document_return(db, return_id)
    if db_return:
        for key, value in return_obj.model_dump(exclude_unset=True).items():
            setattr(db_return, key, value)
        db.commit()
        db.refresh(db_return)
    return db_return


def delete_document_return(db: Session, return_id: int):
    db_return = get_document_return(db, return_id)
    if db_return:
        db.delete(db_return)
        db.commit()
    return db_return