from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class RemarkStatus(str, Enum):
    """Перечисление статусов замечаний"""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    FIXED = "fixed"
    VERIFIED = "verified"
    CLOSED = "closed"
    REJECTED = "rejected"


class ConstructionRemarkBase(BaseModel):
    """Базовая схема для замечаний"""
    remark_number: str
    project_object_id: int
    title: str
    description: str
    status: RemarkStatus = RemarkStatus.NEW
    priority: str = "normal"  # low, normal, high, critical
    assigned_to: Optional[str] = None
    deadline: Optional[datetime] = None
    created_by: str


class ConstructionRemarkCreate(ConstructionRemarkBase):
    """Схема для создания замечания"""
    pass


class ConstructionRemarkUpdate(BaseModel):
    """Схема для обновления замечания"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[RemarkStatus] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    deadline: Optional[datetime] = None


class ConstructionRemark(ConstructionRemarkBase):
    """Схема для чтения замечания"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RemarkPhotoBase(BaseModel):
    """Базовая схема для фотографий замечаний"""
    remark_id: int
    file_path: str
    filename: str
    file_size: int
    description: Optional[str] = None
    created_by: str


class RemarkPhotoCreate(RemarkPhotoBase):
    """Схема для создания фотографии к замечанию"""
    pass


class RemarkPhotoUpdate(BaseModel):
    """Схема для обновления фотографии к замечанию"""
    description: Optional[str] = None


class RemarkPhoto(RemarkPhotoBase):
    """Схема для чтения фотографии к замечанию"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RemarkHistoryBase(BaseModel):
    """Базовая схема для истории изменений замечаний"""
    remark_id: int
    old_status: Optional[RemarkStatus] = None
    new_status: RemarkStatus
    comment: Optional[str] = None
    changed_by: str


class RemarkHistoryCreate(RemarkHistoryBase):
    """Схема для создания записи истории изменения"""
    pass


class RemarkHistory(RemarkHistoryBase):
    """Схема для чтения записи истории изменения"""
    id: int
    changed_at: datetime

    class Config:
        from_attributes = True


class ConstructionRemarkWithDetails(ConstructionRemark):
    """Схема для замечания с деталями"""
    photos: List[RemarkPhoto] = []
    history: List[RemarkHistory] = []

    class Config:
        from_attributes = True