from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import json

from .. import crud, models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(
    prefix="/api/documents",
    tags=["documents"],
    responses={404: {"description": "Not found"}},
)


@router.get("/types", response_model=List[schemas.DocumentType])
def get_document_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить список типов документов
    """
    types = crud.get_document_types(db, skip=skip, limit=limit)
    return types


@router.post("/types", response_model=schemas.DocumentType)
def create_document_type(
    doc_type: schemas.DocumentTypeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Создать новый тип документа
    """
    db_doc_type = crud.create_document_type(db, doc_type)
    return db_doc_type


@router.get("/types/{document_type_id}", response_model=schemas.DocumentType)
def get_document_type(
    document_type_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить тип документа по ID
    """
    doc_type = crud.get_document_type(db, document_type_id)
    if not doc_type:
        raise HTTPException(status_code=404, detail="Тип документа не найден")
    return doc_type


@router.put("/types/{document_type_id}", response_model=schemas.DocumentType)
def update_document_type(
    document_type_id: int,
    doc_type: schemas.DocumentTypeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Обновить тип документа
    """
    db_doc_type = crud.update_document_type(db, document_type_id, doc_type)
    if not db_doc_type:
        raise HTTPException(status_code=404, detail="Тип документа не найден")
    return db_doc_type


@router.delete("/types/{document_type_id}")
def delete_document_type(
    document_type_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Удалить тип документа
    """
    doc_type = crud.get_document_type(db, document_type_id)
    if not doc_type:
        raise HTTPException(status_code=404, detail="Тип документа не найден")
    
    # Проверим, есть ли документы этого типа
    documents = db.query(models.Document).filter(models.Document.document_type_id == document_type_id).all()
    if documents:
        raise HTTPException(status_code=400, detail="Невозможно удалить тип документа, так как существуют документы этого типа")
    
    crud.delete_document_type(db, document_type_id)
    return {"message": "Тип документа успешно удален"}


@router.get("/", response_model=List[schemas.Document])
def get_documents(
    skip: int = 0,
    limit: int = 100,
    project_id: str = None,
    status: str = None,
    doc_number: str = None,
    title: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить список документов с возможностью фильтрации
    """
    documents = crud.get_documents(
        db, 
        skip=skip, 
        limit=limit, 
        project_id=project_id,
        status=status,
        doc_number=doc_number,
        title=title
    )
    return documents


@router.post("/", response_model=schemas.Document)
def create_document(
    document: schemas.DocumentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Создать новый документ
    """
    db_document = crud.create_document(db, document)
    return db_document


@router.get("/{document_id}", response_model=schemas.DocumentDetailed)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить документ по ID с подробной информацией
    """
    document = crud.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")
    return document


@router.put("/{document_id}", response_model=schemas.Document)
def update_document(
    document_id: int,
    document: schemas.DocumentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Обновить документ
    """
    db_document = crud.update_document(db, document_id, document)
    if not db_document:
        raise HTTPException(status_code=404, detail="Документ не найден")
    return db_document


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Удалить документ
    """
    document = crud.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")
    
    # Проверим, есть ли связанные отправки или возвраты
    shipments = crud.get_document_shipments(db, document_id)
    returns = crud.get_document_returns(db, document_id)
    
    if shipments or returns:
        raise HTTPException(status_code=400, detail="Невозможно удалить документ, так как существуют связанные отправки или возвраты")
    
    crud.delete_document(db, document_id)
    return {"message": "Документ успешно удален"}


@router.get("/{document_id}/shipments", response_model=List[schemas.DocumentShipment])
def get_document_shipments(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить список отправок для документа
    """
    document = crud.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")
    
    shipments = crud.get_document_shipments(db, document_id)
    return shipments


@router.post("/{document_id}/shipments", response_model=schemas.DocumentShipment)
def create_document_shipment(
    document_id: int,
    shipment: schemas.DocumentShipmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Создать новую отправку документа
    """
    # Проверим, что документ существует
    document = crud.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")
    
    # Проверим, что документ еще не отправлен
    if document.status == "shipped":
        raise HTTPException(status_code=400, detail="Документ уже отправлен")
    elif document.status == "returned":
        raise HTTPException(status_code=400, detail="Документ уже был возвратом и не может быть отправлен снова")
    
    # Создадим отправку
    shipment_data = schemas.DocumentShipmentCreate(
        document_id=document_id,
        recipient=shipment.recipient,
        shipment_date=shipment.shipment_date,
        notes=shipment.notes
    )
    
    db_shipment = crud.create_document_shipment(db, shipment_data)
    return db_shipment


@router.get("/{document_id}/returns", response_model=List[schemas.DocumentReturn])
def get_document_returns(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить список возвратов для документа
    """
    document = crud.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")
    
    returns = crud.get_document_returns(db, document_id)
    return returns


@router.post("/{document_id}/returns", response_model=schemas.DocumentReturn)
def create_document_return(
    document_id: int,
    return_obj: schemas.DocumentReturnCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Создать новый возврат документа
    """
    # Проверим, что документ существует
    document = crud.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")
    
    # Проверим, что документ был отправлен
    if document.status != "shipped":
        raise HTTPException(status_code=400, detail="Документ не был отправлен и не может быть возвращен")
    
    # Создадим возврат
    return_data = schemas.DocumentReturnCreate(
        document_id=document_id,
        return_date=return_obj.return_date,
        condition=return_obj.condition,
        notes=return_obj.notes
    )
    
    db_return = crud.create_document_return(db, return_data)
    return db_return


@router.post("/search", response_model=List[schemas.Document])
def search_documents(
    query: str = None,
    project_id: str = None,
    status: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Поиск документов по различным критериям
    """
    documents = crud.search_documents(db, query_str=query, project_id=project_id, status=status)
    return documents