from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import crud_work_session, schemas
from ..auth import get_current_user, get_current_active_user
from ..database import get_db
from ..crud_user import get_user_by_id

router = APIRouter(prefix="/work-sessions", tags=["work-sessions"])


@router.post("/start", response_model=schemas.WorkSessionResponse)
def start_work_session(
    current_user: schemas.UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Начать рабочую сессию
    """
    # Проверяем, есть ли уже активная сессия у пользователя
    active_session = crud_work_session.get_active_work_session(db, current_user.id)
    if active_session:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У вас уже есть активная рабочая сессия"
        )
    
    # Создаем новую сессию
    work_session = crud_work_session.create_work_session(db, current_user.id)
    return work_session


@router.post("/end", response_model=schemas.WorkSessionResponse)
def end_work_session(
    current_user: schemas.UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Завершить рабочую сессию
    """
    # Проверяем, есть ли активная сессия у пользователя
    active_session = crud_work_session.get_active_work_session(db, current_user.id)
    if not active_session:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У вас нет активной рабочей сессии"
        )
    
    # Завершаем сессию
    ended_session = crud_work_session.end_work_session(db, current_user.id)
    return ended_session


@router.get("/current-status", response_model=schemas.WorkSessionSummary)
def get_current_work_status(
    current_user: schemas.UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Получить текущий статус рабочей сессии
    """
    active_session = crud_work_session.get_active_work_session(db, current_user.id)
    
    # Получаем все сессии за сегодня
    today_sessions = crud_work_session.get_work_sessions_for_date(db, current_user.id, date.today())
    today_hours = crud_work_session.calculate_total_work_hours(today_sessions)
    
    return schemas.WorkSessionSummary(
        today_hours=today_hours,
        total_sessions_count=len(today_sessions),
        is_working_now=active_session is not None,
        work_start_time=active_session.start_time if active_session else None
    )


@router.get("/my-sessions", response_model=List[schemas.WorkSessionResponse])
def get_my_work_sessions(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Получить свои рабочие сессии
    """
    sessions = crud_work_session.get_work_sessions_by_user(db, current_user.id, limit)
    return sessions


@router.get("/employees", response_model=List[schemas.EmployeeWithWorkInfo])
def get_all_employees_with_work_info(
    current_user: schemas.UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Получить информацию о всех сотрудниках с данными о работе
    """
    # Только администраторы могут просматривать всех сотрудников
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ разрешен только администраторам"
        )
    
    employees = crud_work_session.get_all_employees_with_work_info(db)
    return employees