from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime, date
from typing import List
from .models.work_session import WorkSession
from .models.user import User


def create_work_session(db: Session, user_id: int) -> WorkSession:
    """Создание новой сессии работы"""
    work_session = WorkSession(user_id=user_id, start_time=datetime.now())
    db.add(work_session)
    db.commit()
    db.refresh(work_session)
    return work_session


def end_work_session(db: Session, user_id: int) -> WorkSession:
    """Завершение активной сессии работы"""
    active_session = get_active_work_session(db, user_id)
    if active_session:
        active_session.end_time = datetime.now()
        active_session.is_active = False
        db.commit()
        db.refresh(active_session)
        return active_session
    return None


def get_active_work_session(db: Session, user_id: int) -> WorkSession:
    """Получение активной сессии работы пользователя"""
    return db.query(WorkSession).filter(
        and_(WorkSession.user_id == user_id, WorkSession.is_active == True)
    ).first()


def get_work_sessions_by_user(db: Session, user_id: int, limit: int = 100) -> List[WorkSession]:
    """Получение всех сессий работы пользователя"""
    return db.query(WorkSession).filter(WorkSession.user_id == user_id).order_by(
        WorkSession.start_time.desc()
    ).limit(limit).all()


def get_all_work_sessions(db: Session, skip: int = 0, limit: int = 100) -> List[WorkSession]:
    """Получение всех сессий работы"""
    return db.query(WorkSession).offset(skip).limit(limit).all()


def get_work_sessions_for_date(db: Session, user_id: int, target_date: date) -> List[WorkSession]:
    """Получение сессий работы за определенную дату"""
    return db.query(WorkSession).filter(
        and_(
            WorkSession.user_id == user_id,
            func.date(WorkSession.start_time) == target_date
        )
    ).all()


def calculate_work_hours_for_session(session: WorkSession) -> float:
    """Вычисление количества отработанных часов для одной сессии"""
    if session.end_time:
        duration = session.end_time - session.start_time
        return duration.total_seconds() / 3600  # Конвертация в часы
    else:
        # Если сессия еще активна, считаем до текущего момента
        duration = datetime.now(session.start_time.tzinfo) - session.start_time
        return duration.total_seconds() / 3600


def calculate_total_work_hours(sessions: List[WorkSession]) -> float:
    """Вычисление общего количества отработанных часов"""
    total_hours = 0
    for session in sessions:
        total_hours += calculate_work_hours_for_session(session)
    return round(total_hours, 2)


def format_duration(hours: float) -> str:
    """Форматирование продолжительности времени"""
    if hours <= 0:
        return "0 ч 0 мин"
    
    total_minutes = int(hours * 60)
    hours_part = total_minutes // 60
    minutes_part = total_minutes % 60
    return f"{hours_part} ч {minutes_part} мин"


def get_all_employees_with_work_info(db: Session) -> List[dict]:
    """Получение информации о всех сотрудниках с данными о работе"""
    employees = db.query(User).filter(User.is_active == True).all()
    result = []
    
    for employee in employees:
        # Получаем последнюю активную сессию
        active_session = get_active_work_session(db, employee.id)
        
        # Получаем все сессии за сегодня
        today_sessions = get_work_sessions_for_date(db, employee.id, date.today())
        today_hours = calculate_total_work_hours(today_sessions)
        
        employee_info = {
            "id": employee.id,
            "username": employee.username,
            "full_name": employee.full_name or employee.username,
            "position": employee.position,
            "department": employee.department,
            "email": employee.email,
            "is_active": employee.is_active,
            "is_working_now": active_session is not None,
            "work_start_time": active_session.start_time if active_session else None,
            "today_hours": today_hours,
            "total_sessions_count": len(today_sessions)
        }
        result.append(employee_info)
    
    return result