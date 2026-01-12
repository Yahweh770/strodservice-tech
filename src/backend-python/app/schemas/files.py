from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Схемы для категорий файлов
class FileCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class FileCategoryCreate(FileCategoryBase):
    pass


class FileCategoryUpdate(FileCategoryBase):
    pass


class FileCategory(FileCategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Схемы для загруженных файлов
class UploadedFileBase(BaseModel):
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    content_type: Optional[str] = None
    category_id: Optional[int] = None
    section_id: Optional[str] = None
    section_name: Optional[str] = None
    project_id: Optional[str] = None
    uploaded_by: str
    description: Optional[str] = None


class UploadedFileCreate(UploadedFileBase):
    pass


class UploadedFileUpdate(BaseModel):
    category_id: Optional[int] = None
    section_id: Optional[str] = None
    section_name: Optional[str] = None
    project_id: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class UploadedFile(UploadedFileBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Схемы для запросов на материалы
class MaterialRequestBase(BaseModel):
    material_id: int
    requested_quantity: int
    needed_quantity: int
    available_quantity: int = 0
    section_id: Optional[str] = None
    section_name: Optional[str] = None
    project_id: Optional[str] = None
    reason: Optional[str] = None
    requested_by: str


class MaterialRequestCreate(MaterialRequestBase):
    pass


class MaterialRequestUpdate(BaseModel):
    status: Optional[str] = None
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    fulfilled_at: Optional[datetime] = None


class MaterialRequest(MaterialRequestBase):
    id: int
    status: str = "pending"
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    fulfilled_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Схемы для остатков материалов
class MaterialStockBase(BaseModel):
    material_id: int
    quantity: int = 0
    reserved_quantity: int = 0
    min_threshold: int = 10
    location: Optional[str] = None


class MaterialStockCreate(MaterialStockBase):
    pass


class MaterialStockUpdate(BaseModel):
    quantity: Optional[int] = None
    reserved_quantity: Optional[int] = None
    min_threshold: Optional[int] = None
    location: Optional[str] = None


class MaterialStock(MaterialStockBase):
    id: int
    created_at: datetime
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True