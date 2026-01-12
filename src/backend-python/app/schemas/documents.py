from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Схемы для типов документов
class DocumentTypeBase(BaseModel):
    name: str
    description: Optional[str] = None


class DocumentTypeCreate(DocumentTypeBase):
    pass


class DocumentTypeUpdate(DocumentTypeBase):
    pass


class DocumentType(DocumentTypeBase):
    id: int

    class Config:
        from_attributes = True


# Схемы для документов
class DocumentBase(BaseModel):
    doc_number: str
    title: str
    project_id: str
    document_type_id: int


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    doc_number: Optional[str] = None
    title: Optional[str] = None
    project_id: Optional[str] = None
    document_type_id: Optional[int] = None


class Document(DocumentBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Схемы для отправок документов
class DocumentShipmentBase(BaseModel):
    document_id: int
    recipient: str
    shipment_date: datetime
    notes: Optional[str] = None


class DocumentShipmentCreate(DocumentShipmentBase):
    pass


class DocumentShipmentUpdate(BaseModel):
    recipient: Optional[str] = None
    shipment_date: Optional[datetime] = None
    notes: Optional[str] = None


class DocumentShipment(DocumentShipmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Схемы для возвратов документов
class DocumentReturnBase(BaseModel):
    document_id: int
    return_date: datetime
    condition: str
    notes: Optional[str] = None


class DocumentReturnCreate(DocumentReturnBase):
    pass


class DocumentReturnUpdate(BaseModel):
    return_date: Optional[datetime] = None
    condition: Optional[str] = None
    notes: Optional[str] = None


class DocumentReturn(DocumentReturnBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Расширенная схема документа с информацией о связях
class DocumentDetailed(Document):
    type: DocumentType
    shipments: List[DocumentShipment] = []
    returns: List[DocumentReturn] = []

    class Config:
        from_attributes = True