from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
import shutil
from pathlib import Path

from ..database import get_db
from .. import schemas, crud_construction_remarks, crud
from ..auth import get_current_user, get_current_active_user

router = APIRouter(
    prefix="/construction-remarks",
    tags=["construction-remarks"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.ConstructionRemark)
async def create_construction_remark(
    remark: schemas.ConstructionRemarkCreate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Создать новое замечание от строительного контроля"""
    # Проверяем, существует ли объект проекта
    project_object = crud.get_project_object(db, remark.project_object_id)
    if not project_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объект проекта не найден"
        )
    
    # Проверяем, существует ли уже замечание с таким номером
    existing_remark = crud_construction_remarks.get_construction_remark_by_number(db, remark.remark_number)
    if existing_remark:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Замечание с таким номером уже существует"
        )
    
    # Создаем замечание
    remark.created_by = current_user.username
    db_remark = crud_construction_remarks.create_construction_remark(db, remark)
    return db_remark


@router.get("/{remark_id}", response_model=schemas.ConstructionRemarkWithDetails)
async def get_construction_remark(
    remark_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить замечание по ID с деталями"""
    remark = crud_construction_remarks.get_construction_remark(db, remark_id)
    if not remark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Замечание не найдено"
        )
    
    # Добавляем фотографии и историю к замечанию
    remark.photos = crud_construction_remarks.get_remark_photos(db, remark_id)
    remark.history = crud_construction_remarks.get_remark_history(db, remark_id)
    return remark


@router.put("/{remark_id}", response_model=schemas.ConstructionRemark)
async def update_construction_remark(
    remark_id: int,
    remark_update: schemas.ConstructionRemarkUpdate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Обновить замечание"""
    db_remark = crud_construction_remarks.get_construction_remark(db, remark_id)
    if not db_remark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Замечание не найдено"
        )
    
    # Обновляем замечание
    updated_remark = crud_construction_remarks.update_construction_remark(db, remark_id, remark_update)
    return updated_remark


@router.delete("/{remark_id}")
async def delete_construction_remark(
    remark_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Удалить замечание"""
    db_remark = crud_construction_remarks.get_construction_remark(db, remark_id)
    if not db_remark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Замечание не найдено"
        )
    
    # Проверяем права (например, только администраторы могут удалять)
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для удаления замечания"
        )
    
    crud_construction_remarks.delete_construction_remark(db, remark_id)
    return {"message": "Замечание успешно удалено"}


@router.get("/", response_model=List[schemas.ConstructionRemark])
async def get_construction_remarks(
    skip: int = 0,
    limit: int = 100,
    project_object_id: Optional[int] = None,
    status: Optional[schemas.RemarkStatus] = None,
    priority: Optional[str] = None,
    assigned_to: Optional[str] = None,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить список замечаний с фильтрами"""
    remarks = crud_construction_remarks.get_construction_remarks(
        db, skip=skip, limit=limit,
        project_object_id=project_object_id,
        status=status,
        priority=priority,
        assigned_to=assigned_to
    )
    return remarks


@router.get("/search", response_model=List[schemas.ConstructionRemark])
async def search_construction_remarks(
    query: str,
    project_object_id: Optional[int] = None,
    status: Optional[schemas.RemarkStatus] = None,
    priority: Optional[str] = None,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Поиск замечаний по различным критериям"""
    remarks = crud_construction_remarks.search_construction_remarks(
        db,
        query_str=query,
        project_object_id=project_object_id,
        status=status,
        priority=priority
    )
    return remarks


@router.get("/project-object/{project_object_id}", response_model=List[schemas.ConstructionRemark])
async def get_remarks_by_project_object(
    project_object_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить все замечания для конкретного объекта проекта"""
    # Проверяем, существует ли объект проекта
    project_obj = crud.get_project_object(db, project_object_id)
    if not project_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объект проекта не найден"
        )
    
    remarks = crud_construction_remarks.get_remarks_by_project_object(db, project_object_id)
    return remarks


@router.get("/project-object/{project_object_id}/summary")
async def get_remarks_summary_by_project_object(
    project_object_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить сводку по замечаниям для объекта проекта"""
    # Проверяем, существует ли объект проекта
    project_obj = crud.get_project_object(db, project_object_id)
    if not project_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объект проекта не найден"
        )
    
    summary = crud_construction_remarks.get_remarks_summary_by_project_object(db, project_object_id)
    return summary


@router.get("/status/{status}", response_model=List[schemas.ConstructionRemark])
async def get_remarks_by_status(
    status: schemas.RemarkStatus,
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить все замечания с определенным статусом"""
    remarks = crud_construction_remarks.get_remarks_by_status(db, status)
    return remarks


@router.get("/overdue", response_model=List[schemas.ConstructionRemark])
async def get_overdue_remarks(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить все просроченные замечания"""
    remarks = crud_construction_remarks.get_overdue_remarks(db)
    return remarks


# Маршруты для фотографий к замечаниям
@router.post("/{remark_id}/photos", response_model=schemas.RemarkPhoto)
async def upload_remark_photo(
    remark_id: int,
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Загрузить фотографию к замечанию"""
    # Проверяем, существует ли замечание
    remark = crud_construction_remarks.get_construction_remark(db, remark_id)
    if not remark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Замечание не найдено"
        )
    
    # Создаем директорию для хранения фотографий, если не существует
    photos_dir = Path("uploads/remark_photos")
    photos_dir.mkdir(parents=True, exist_ok=True)
    
    # Формируем имя файла
    file_extension = Path(file.filename).suffix
    filename = f"remark_{remark_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    file_path = photos_dir / filename
    
    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Создаем запись в базе данных
    photo_create = schemas.RemarkPhotoCreate(
        remark_id=remark_id,
        file_path=str(file_path),
        filename=filename,
        file_size=file.file.tell(),  # Размер файла
        description=description,
        created_by=current_user.username
    )
    
    # Сбрасываем указатель файла, чтобы получить правильный размер
    file.file.seek(0)
    photo_create.file_size = len(file.file.read())
    file.file.seek(0)
    
    db_photo = crud_construction_remarks.create_remark_photo(db, photo_create)
    return db_photo


@router.get("/{remark_id}/photos", response_model=List[schemas.RemarkPhoto])
async def get_remark_photos(
    remark_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить все фотографии для замечания"""
    # Проверяем, существует ли замечание
    remark = crud_construction_remarks.get_construction_remark(db, remark_id)
    if not remark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Замечание не найдено"
        )
    
    photos = crud_construction_remarks.get_remark_photos(db, remark_id)
    return photos


@router.put("/photos/{photo_id}", response_model=schemas.RemarkPhoto)
async def update_remark_photo(
    photo_id: int,
    photo_update: schemas.RemarkPhotoUpdate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Обновить описание фотографии"""
    db_photo = crud_construction_remarks.get_remark_photo(db, photo_id)
    if not db_photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фотография не найдена"
        )
    
    updated_photo = crud_construction_remarks.update_remark_photo(db, photo_id, photo_update)
    return updated_photo


@router.delete("/photos/{photo_id}")
async def delete_remark_photo(
    photo_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Удалить фотографию из замечания"""
    db_photo = crud_construction_remarks.get_remark_photo(db, photo_id)
    if not db_photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фотография не найдена"
        )
    
    # Проверяем права (например, только администраторы могут удалять)
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для удаления фотографии"
        )
    
    # Удаляем файл с диска
    if os.path.exists(db_photo.file_path):
        os.remove(db_photo.file_path)
    
    crud_construction_remarks.delete_remark_photo(db, photo_id)
    return {"message": "Фотография успешно удалена"}


# Маршрут для получения истории изменений замечания
@router.get("/{remark_id}/history", response_model=List[schemas.RemarkHistory])
async def get_remark_history(
    remark_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получить историю изменений статуса замечания"""
    # Проверяем, существует ли замечание
    remark = crud_construction_remarks.get_construction_remark(db, remark_id)
    if not remark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Замечание не найдено"
        )
    
    history = crud_construction_remarks.get_remark_history(db, remark_id)
    return history