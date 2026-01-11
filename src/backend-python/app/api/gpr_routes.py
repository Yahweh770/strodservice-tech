from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import json

from .. import crud, models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(
    prefix="/api/gpr",
    tags=["gpr"],
    responses={404: {"description": "Not found"}},
)


@router.get("/records", response_model=List[schemas.GPRRecord])
def get_gpr_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить список записей ГПР
    """
    records = crud.get_gpr_records(db, skip=skip, limit=limit)
    return records


@router.post("/records", response_model=schemas.GPRRecord)
def create_gpr_record(
    record: schemas.GPRRecordCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Создать новую запись ГПР
    """
    # Вычисляем остаток и прогресс при создании записи
    volume_remainder = record.volume_plan - record.volume_fact
    progress = 0
    if record.volume_plan > 0:
        progress = round((record.volume_fact / record.volume_plan) * 100, 2)
    
    db_record = models.GPRRecord(
        customer_id=record.customer_id,
        object_id=record.object_id,
        work_type=record.work_type,
        volume_plan=record.volume_plan,
        volume_fact=record.volume_fact,
        volume_remainder=volume_remainder,
        progress=progress,
        daily_data=json.dumps(record.daily_data) if record.daily_data else "{}"
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


@router.put("/records/{record_id}", response_model=schemas.GPRRecord)
def update_gpr_record(
    record_id: int,
    record: schemas.GPRRecordUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Обновить запись ГПР
    """
    db_record = crud.get_gpr_record(db, record_id=record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Запись ГПР не найдена")
    
    # Обновляем поля
    update_data = record.dict(exclude_unset=True)
    
    # Если обновляется объем плана или факт, пересчитываем остаток и прогресс
    if 'volume_plan' in update_data or 'volume_fact' in update_data:
        volume_plan = update_data.get('volume_plan', db_record.volume_plan)
        volume_fact = update_data.get('volume_fact', db_record.volume_fact)
        
        volume_remainder = volume_plan - volume_fact
        progress = 0
        if volume_plan > 0:
            progress = round((volume_fact / volume_plan) * 100, 2)
        
        update_data['volume_remainder'] = volume_remainder
        update_data['progress'] = progress
    
    # Если обновляются ежедневные данные, преобразуем в JSON
    if 'daily_data' in update_data:
        update_data['daily_data'] = json.dumps(update_data['daily_data'])
    
    for field, value in update_data.items():
        setattr(db_record, field, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record


@router.delete("/records/{record_id}")
def delete_gpr_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Удалить запись ГПР
    """
    record = crud.get_gpr_record(db, record_id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Запись ГПР не найдена")
    
    db.delete(record)
    db.commit()
    return {"message": "Запись ГПР успешно удалена"}


@router.post("/weekly-report")
def generate_weekly_report(
    week_start_date: str,
    created_by: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Сгенерировать недельный отчет
    """
    try:
        week_start = datetime.strptime(week_start_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты. Используйте YYYY-MM-DD")
    
    # Получаем все записи ГПР
    all_records = crud.get_gpr_records(db, skip=0, limit=1000)
    
    # Подготовим данные для недельного отчета
    materials = [
        "kraska_b", "kraska_ch", "vremyanka", "kraska_j", 
        "hp", "hpj", "tp", "demarkirovka"
    ]
    
    report_data = []
    for material in materials:
        # Суммируем план и факт по каждому материалу
        total_plan = sum(r.volume_plan for r in all_records if r.work_type == material)
        total_fact = sum(r.volume_fact for r in all_records if r.work_type == material)
        
        report_data.append({
            "material": material,
            "plan": total_plan,
            "fact": total_fact
        })
    
    # Сохраняем недельный отчет в базе данных
    weekly_report = models.WeeklyReport(
        week_start_date=datetime.combine(week_start, datetime.min.time()),
        report_data=json.dumps(report_data),
        created_by=created_by
    )
    db.add(weekly_report)
    db.commit()
    
    return {
        "week_start_date": week_start,
        "report_data": report_data,
        "created_by": created_by
    }


@router.get("/weekly-report/{week_start_date}")
def get_weekly_report(
    week_start_date: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить недельный отчет за определенную неделю
    """
    try:
        week_start = datetime.strptime(week_start_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты. Используйте YYYY-MM-DD")
    
    # Ищем отчет за указанную неделю
    report = crud.get_weekly_report_by_date(db, week_start)
    if not report:
        raise HTTPException(status_code=404, detail="Недельный отчет не найден")
    
    return {
        "week_start_date": report.week_start_date,
        "report_data": json.loads(report.report_data),
        "created_by": report.created_by
    }