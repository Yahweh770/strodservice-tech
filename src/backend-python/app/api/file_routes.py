from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os
from datetime import datetime
import shutil

from .. import crud, models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(
    prefix="/api/files",
    tags=["files"],
    responses={404: {"description": "Not found"}},
)


@router.get("/categories", response_model=List[schemas.FileCategory])
def get_file_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить список категорий файлов
    """
    categories = crud.get_file_categories(db, skip=skip, limit=limit)
    return categories


@router.post("/categories", response_model=schemas.FileCategory)
def create_file_category(
    category: schemas.FileCategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Создать новую категорию файлов
    """
    db_category = crud.create_file_category(db, category)
    return db_category


@router.get("/categories/{category_id}", response_model=schemas.FileCategory)
def get_file_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить категорию файлов по ID
    """
    category = crud.get_file_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория файлов не найдена")
    return category


@router.put("/categories/{category_id}", response_model=schemas.FileCategory)
def update_file_category(
    category_id: int,
    category: schemas.FileCategoryUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Обновить категорию файлов
    """
    db_category = crud.update_file_category(db, category_id, category)
    if not db_category:
        raise HTTPException(status_code=404, detail="Категория файлов не найдена")
    return db_category


@router.delete("/categories/{category_id}")
def delete_file_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Удалить категорию файлов
    """
    category = crud.get_file_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория файлов не найдена")
    
    # Проверим, есть ли файлы этой категории
    files = db.query(models.UploadedFile).filter(models.UploadedFile.category_id == category_id).all()
    if files:
        raise HTTPException(status_code=400, detail="Невозможно удалить категорию, так как существуют файлы этой категории")
    
    crud.delete_file_category(db, category_id)
    return {"message": "Категория файлов успешно удалена"}


@router.get("/", response_model=List[schemas.UploadedFile])
def get_uploaded_files(
    skip: int = 0,
    limit: int = 100,
    section_id: str = None,
    project_id: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить список загруженных файлов с возможностью фильтрации
    """
    files = crud.get_uploaded_files(db, skip=skip, limit=limit, section_id=section_id, project_id=project_id)
    return files


@router.post("/", response_model=schemas.UploadedFile)
def upload_file(
    file: UploadFile = File(...),
    category_id: int = Form(None),
    section_id: str = Form(None),
    section_name: str = Form(None),
    project_id: str = Form(None),
    description: str = Form(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Загрузить новый файл
    """
    # Создаем директорию для файлов если её нет
    upload_dir = "/workspace/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Генерируем уникальное имя файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_filename = file.filename
    file_ext = os.path.splitext(original_filename)[1]
    filename = f"{timestamp}_{original_filename}"
    file_path = os.path.join(upload_dir, filename)
    
    # Получаем размер файла до сохранения
    file.file.seek(0, 2)  # Перемещаемся в конец файла
    file_size = file.file.tell()  # Получаем размер
    file.file.seek(0)  # Возвращаем указатель в начало
    
    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Создаем запись о файле в базе данных
    file_create = schemas.UploadedFileCreate(
        filename=filename,
        original_filename=original_filename,
        file_path=file_path,
        file_size=file_size,
        content_type=file.content_type,
        category_id=category_id,
        section_id=section_id,
        section_name=section_name,
        project_id=project_id,
        uploaded_by=current_user.get("username", "unknown"),
        description=description
    )
    
    db_file = crud.create_uploaded_file(db, file_create)
    return db_file


@router.get("/{file_id}", response_model=schemas.UploadedFile)
def get_uploaded_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить информацию о загруженном файле по ID
    """
    file = crud.get_uploaded_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")
    return file


@router.put("/{file_id}", response_model=schemas.UploadedFile)
def update_uploaded_file(
    file_id: int,
    file_update: schemas.UploadedFileUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Обновить информацию о загруженном файле
    """
    db_file = crud.update_uploaded_file(db, file_id, file_update)
    if not db_file:
        raise HTTPException(status_code=404, detail="Файл не найден")
    return db_file


@router.delete("/{file_id}")
def delete_uploaded_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Удалить загруженный файл
    """
    file = crud.get_uploaded_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    # Удаляем файл с диска
    if os.path.exists(file.file_path):
        os.remove(file.file_path)
    
    crud.delete_uploaded_file(db, file_id)
    return {"message": "Файл успешно удален"}


@router.get("/{file_id}/download")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Скачать файл
    """
    file = crud.get_uploaded_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    if not os.path.exists(file.file_path):
        raise HTTPException(status_code=404, detail="Файл не найден на диске")
    
    return {"file_path": file.file_path, "filename": file.original_filename}


# Маршруты для запросов на материалы
@router.get("/material-requests", response_model=List[schemas.MaterialRequest])
def get_material_requests(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    section_id: str = None,
    project_id: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить список запросов на материалы
    """
    requests = crud.get_material_requests(db, skip=skip, limit=limit, status=status, section_id=section_id, project_id=project_id)
    return requests


@router.post("/material-requests", response_model=schemas.MaterialRequest)
def create_material_request(
    request: schemas.MaterialRequestCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Создать новый запрос на материалы
    """
    # Проверяем, достаточно ли материалов на складе
    stock = crud.get_material_stock_by_material(db, request.material_id)
    if stock:
        available = stock.quantity - stock.reserved_quantity
        if available < request.needed_quantity:
            # Автоматически обновляем доступное количество
            request.available_quantity = available
        else:
            request.available_quantity = available
    
    # Устанавливаем пользователя, который сделал запрос
    request.requested_by = current_user.get("username", "unknown")
    
    db_request = crud.create_material_request(db, request)
    return db_request


@router.get("/material-requests/{request_id}", response_model=schemas.MaterialRequest)
def get_material_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить запрос на материалы по ID
    """
    request = crud.get_material_request(db, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Запрос на материалы не найден")
    return request


@router.put("/material-requests/{request_id}", response_model=schemas.MaterialRequest)
def update_material_request(
    request_id: int,
    request_update: schemas.MaterialRequestUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Обновить запрос на материалы
    """
    # Если запрос одобряется, обновляем информацию об этом
    if request_update.status == "approved":
        request_update.approved_by = current_user.get("username", "unknown")
        request_update.approved_at = datetime.utcnow()
    elif request_update.status == "fulfilled":
        request_update.fulfilled_at = datetime.utcnow()
    
    db_request = crud.update_material_request(db, request_id, request_update)
    if not db_request:
        raise HTTPException(status_code=404, detail="Запрос на материалы не найден")
    return db_request


# Маршруты для управления остатками материалов
@router.get("/material-stocks", response_model=List[schemas.MaterialStock])
def get_material_stocks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить список остатков материалов
    """
    stocks = crud.get_material_stocks(db, skip=skip, limit=limit)
    return stocks


@router.get("/material-stocks/{stock_id}", response_model=schemas.MaterialStock)
def get_material_stock(
    stock_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить остаток материала по ID
    """
    stock = crud.get_material_stock(db, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Остаток материала не найден")
    return stock


@router.get("/material-stocks/by-material/{material_id}", response_model=schemas.MaterialStock)
def get_material_stock_by_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить остаток материала по ID материала
    """
    stock = crud.get_material_stock_by_material(db, material_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Остаток материала не найден")
    return stock


@router.post("/material-stocks", response_model=schemas.MaterialStock)
def create_material_stock(
    stock: schemas.MaterialStockCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Создать новую запись об остатке материала
    """
    db_stock = crud.create_material_stock(db, stock)
    return db_stock


@router.put("/material-stocks/{stock_id}", response_model=schemas.MaterialStock)
def update_material_stock(
    stock_id: int,
    stock_update: schemas.MaterialStockUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Обновить остаток материала
    """
    db_stock = crud.update_material_stock(db, stock_id, stock_update)
    if not db_stock:
        raise HTTPException(status_code=404, detail="Остаток материала не найден")
    return db_stock


@router.get("/low-stock-materials")
def get_low_stock_materials(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить список материалов с низким уровнем запасов
    """
    low_stock_materials = crud.get_low_stock_materials(db)
    return {"low_stock_materials": low_stock_materials}


@router.post("/check-material-threshold/{material_id}")
def check_material_threshold(
    material_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Проверить, достигнут ли минимальный порог для материала
    """
    is_low = crud.check_material_threshold(db, material_id)
    return {"material_id": material_id, "is_below_threshold": is_low}