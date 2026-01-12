from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
from ..database import Base


class DocumentType(Base):
    """
    Модель для справочника типов документов
    """
    __tablename__ = "document_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)  # Название типа документа
    description = Column(Text, nullable=True)                      # Описание типа документа
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Document(Base):
    """
    Модель для хранения информации об исполнительной документации
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    doc_number = Column(String, index=True, nullable=False)          # Номер документа
    title = Column(Text, index=True, nullable=False)                 # Наименование документа
    project_id = Column(String, index=True, nullable=False)          # ID проекта (согласно архитектуре)
    document_type_id = Column(Integer, ForeignKey("document_types.id"), index=True, nullable=False)  # Тип документа
    status = Column(String, index=True, default="in_office")         # Статус документа: in_office, shipped, returned
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    type = relationship("DocumentType", back_populates="documents")
    shipments = relationship("DocumentShipment", back_populates="document")
    returns = relationship("DocumentReturn", back_populates="document")


class DocumentShipment(Base):
    """
    Модель для хранения информации об отправках документов
    """
    __tablename__ = "document_shipments"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    recipient = Column(String, nullable=False)           # Получатель
    shipment_date = Column(DateTime, nullable=False)     # Дата отправки
    notes = Column(Text, nullable=True)                  # Примечания
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    document = relationship("Document", back_populates="shipments")


class DocumentReturn(Base):
    """
    Модель для хранения информации о возвратах документов
    """
    __tablename__ = "document_returns"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    return_date = Column(DateTime, nullable=False)       # Дата возврата
    condition = Column(String, nullable=False)           # Состояние документа при возврате
    notes = Column(Text, nullable=True)                  # Примечания
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    document = relationship("Document", back_populates="returns")


# Добавим связи в DocumentType
DocumentType.documents = relationship("Document", back_populates="type")