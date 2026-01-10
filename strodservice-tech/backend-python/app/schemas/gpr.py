from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class GPRRecordBase(BaseModel):
    customer_id: str
    object_id: str
    work_type: str
    volume_plan: float
    volume_fact: float = 0.0
    volume_remainder: float = 0.0
    progress: float = 0.0
    daily_data: Optional[Dict[str, Any]] = None


class GPRRecordCreate(GPRRecordBase):
    pass


class GPRRecordUpdate(BaseModel):
    customer_id: Optional[str] = None
    object_id: Optional[str] = None
    work_type: Optional[str] = None
    volume_plan: Optional[float] = None
    volume_fact: Optional[float] = None
    volume_remainder: Optional[float] = None
    progress: Optional[float] = None
    daily_data: Optional[Dict[str, Any]] = None


class GPRRecord(GPRRecordBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WeeklyReportBase(BaseModel):
    week_start_date: datetime
    report_data: str
    created_by: str


class WeeklyReportCreate(WeeklyReportBase):
    pass


class WeeklyReport(WeeklyReportBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MaterialBase(BaseModel):
    name: str
    description: Optional[str] = None


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class Material(MaterialBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True