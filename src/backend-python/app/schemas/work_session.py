from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .user import UserResponse


class WorkSessionBase(BaseModel):
    user_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    is_active: bool = True


class WorkSessionCreate(BaseModel):
    pass  # Для начала сессии не требуется дополнительных данных


class WorkSessionEnd(BaseModel):
    pass  # Для завершения сессии не требуется дополнительных данных


class WorkSessionResponse(WorkSessionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True


class WorkSessionSummary(BaseModel):
    today_hours: float
    total_sessions_count: int
    is_working_now: bool
    work_start_time: Optional[datetime] = None


class EmployeeWithWorkInfo(BaseModel):
    id: int
    username: str
    full_name: str
    position: Optional[str] = None
    department: Optional[str] = None
    email: Optional[str] = None
    is_active: bool
    is_working_now: bool
    work_start_time: Optional[datetime] = None
    today_hours: float
    total_sessions_count: int

    class Config:
        from_attributes = True