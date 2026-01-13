from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime
from . import models, schemas


def get_construction_remark(db: Session, remark_id: int):
    """Получить замечание по ID"""
    return db.query(models.ConstructionRemark).filter(models.ConstructionRemark.id == remark_id).first()


def get_construction_remark_by_number(db: Session, remark_number: str):
    """Получить замечание по номеру"""
    return db.query(models.ConstructionRemark).filter(models.ConstructionRemark.remark_number == remark_number).first()


def get_construction_remarks(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    project_object_id: Optional[int] = None, 
    status: Optional[schemas.RemarkStatus] = None,
    priority: Optional[str] = None,
    assigned_to: Optional[str] = None
):
    """Получить список замечаний с фильтрами"""
    query = db.query(models.ConstructionRemark)
    
    if project_object_id:
        query = query.filter(models.ConstructionRemark.project_object_id == project_object_id)
    if status:
        query = query.filter(models.ConstructionRemark.status == status)
    if priority:
        query = query.filter(models.ConstructionRemark.priority == priority)
    if assigned_to:
        query = query.filter(models.ConstructionRemark.assigned_to == assigned_to)
        
    return query.offset(skip).limit(limit).all()


def create_construction_remark(db: Session, remark: schemas.ConstructionRemarkCreate):
    """Создать новое замечание"""
    db_remark = models.ConstructionRemark(**remark.dict())
    db.add(db_remark)
    db.commit()
    db.refresh(db_remark)
    
    # Создаем запись в истории после того, как замечание сохранено
    history_entry = models.RemarkHistory(
        remark_id=db_remark.id,
        old_status=None,
        new_status=remark.status,
        comment=f"Замечание создано",
        changed_by=remark.created_by
    )
    db.add(history_entry)
    db.commit()
    
    return db_remark


def update_construction_remark(db: Session, remark_id: int, remark_update: schemas.ConstructionRemarkUpdate):
    """Обновить замечание"""
    db_remark = get_construction_remark(db, remark_id)
    if db_remark:
        # Сохраняем старый статус для истории
        old_status = db_remark.status
        
        # Обновляем замечание
        update_data = remark_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_remark, field, value)
        
        # Если статус изменился, создаем запись в истории
        if 'status' in update_data and old_status != update_data['status']:
            history_entry = models.RemarkHistory(
                remark_id=remark_id,
                old_status=old_status,
                new_status=update_data['status'],
                comment=f"Статус изменен с {old_status.value} на {update_data['status'].value}",
                changed_by=db_remark.created_by  # В реальном приложении нужно передавать пользователя
            )
            db.add(history_entry)
        
        db.commit()
        db.refresh(db_remark)
    return db_remark


def delete_construction_remark(db: Session, remark_id: int):
    """Удалить замечание"""
    db_remark = get_construction_remark(db, remark_id)
    if db_remark:
        db.delete(db_remark)
        db.commit()
    return db_remark


def search_construction_remarks(
    db: Session, 
    query_str: Optional[str] = None, 
    project_object_id: Optional[int] = None, 
    status: Optional[schemas.RemarkStatus] = None,
    priority: Optional[str] = None
):
    """Поиск замечаний по различным критериям"""
    db_query = db.query(models.ConstructionRemark)
    
    if query_str:
        # Поиск по номеру замечания, заголовку или описанию
        db_query = db_query.filter(
            or_(
                models.ConstructionRemark.remark_number.contains(query_str),
                models.ConstructionRemark.title.contains(query_str),
                models.ConstructionRemark.description.contains(query_str)
            )
        )
    
    if project_object_id:
        db_query = db_query.filter(models.ConstructionRemark.project_object_id == project_object_id)
    
    if status:
        db_query = db_query.filter(models.ConstructionRemark.status == status)
    
    if priority:
        db_query = db_query.filter(models.ConstructionRemark.priority == priority)
    
    return db_query.all()


def get_remark_photos(db: Session, remark_id: int):
    """Получить все фотографии для замечания"""
    return db.query(models.RemarkPhoto).filter(models.RemarkPhoto.remark_id == remark_id).all()


def get_remark_photo(db: Session, photo_id: int):
    """Получить фотографию по ID"""
    return db.query(models.RemarkPhoto).filter(models.RemarkPhoto.id == photo_id).first()


def create_remark_photo(db: Session, photo: schemas.RemarkPhotoCreate):
    """Создать новую фотографию для замечания"""
    db_photo = models.RemarkPhoto(**photo.dict())
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo


def update_remark_photo(db: Session, photo_id: int, photo_update: schemas.RemarkPhotoUpdate):
    """Обновить фотографию"""
    db_photo = get_remark_photo(db, photo_id)
    if db_photo:
        update_data = photo_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_photo, field, value)
        db.commit()
        db.refresh(db_photo)
    return db_photo


def delete_remark_photo(db: Session, photo_id: int):
    """Удалить фотографию"""
    db_photo = get_remark_photo(db, photo_id)
    if db_photo:
        db.delete(db_photo)
        db.commit()
    return db_photo


def get_remark_history(db: Session, remark_id: int):
    """Получить историю изменений замечания"""
    return db.query(models.RemarkHistory).filter(models.RemarkHistory.remark_id == remark_id).order_by(models.RemarkHistory.changed_at.desc()).all()


def create_remark_history(db: Session, history: schemas.RemarkHistoryCreate):
    """Создать запись в истории изменения замечания"""
    db_history = models.RemarkHistory(**history.dict())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history


def get_remarks_by_project_object(db: Session, project_object_id: int):
    """Получить все замечания для конкретного объекта проекта"""
    return db.query(models.ConstructionRemark).filter(
        models.ConstructionRemark.project_object_id == project_object_id
    ).all()


def get_remarks_by_status(db: Session, status: schemas.RemarkStatus):
    """Получить все замечания с определенным статусом"""
    return db.query(models.ConstructionRemark).filter(
        models.ConstructionRemark.status == status
    ).all()


def get_overdue_remarks(db: Session):
    """Получить все просроченные замечания"""
    from sqlalchemy import and_
    return db.query(models.ConstructionRemark).filter(
        and_(
            models.ConstructionRemark.deadline < datetime.utcnow(),
            models.ConstructionRemark.status != schemas.RemarkStatus.FIXED,
            models.ConstructionRemark.status != schemas.RemarkStatus.CLOSED,
            models.ConstructionRemark.status != schemas.RemarkStatus.VERIFIED
        )
    ).all()


def get_remarks_summary_by_project_object(db: Session, project_object_id: int):
    """Получить сводку по замечаниям для объекта проекта"""
    from sqlalchemy import func
    
    summary = db.query(
        models.ConstructionRemark.status,
        func.count(models.ConstructionRemark.id).label('count')
    ).filter(
        models.ConstructionRemark.project_object_id == project_object_id
    ).group_by(
        models.ConstructionRemark.status
    ).all()
    
    return {
        'total': db.query(models.ConstructionRemark).filter(
            models.ConstructionRemark.project_object_id == project_object_id
        ).count(),
        'by_status': {item.status.value: item.count for item in summary}
    }