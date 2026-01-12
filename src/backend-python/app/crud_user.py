from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional
from . import models, schemas, auth
from datetime import datetime


def get_user_by_username(db: Session, username: str):
    """Получить пользователя по имени пользователя"""
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """Получить пользователя по email"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user(db: Session, user_id: int):
    """Получить пользователя по ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Получить список пользователей"""
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """Создать нового пользователя"""
    # Проверяем, существует ли уже пользователь с таким именем или email
    existing_user = db.query(models.User).filter(
        or_(models.User.username == user.username, 
            models.User.email == user.email if user.email else False)
    ).first()
    
    if existing_user:
        raise ValueError("Пользователь с таким именем или email уже существует")
    
    # Хешируем пароль
    hashed_password = auth.get_password_hash(user.password)
    
    # Создаем пользователя
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        position=user.position,
        department=user.department,
        hashed_password=hashed_password,
        is_active=user.is_active,
        is_admin=user.is_admin,
        permissions=str(user.permissions)  # Сохраняем как строку JSON
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    """Обновить информацию о пользователе"""
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        
        # Если есть новый пароль, нужно его захешировать
        if "password" in update_data:
            update_data["hashed_password"] = auth.get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            if field != "password":
                setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
    
    return db_user


def delete_user(db: Session, user_id: int):
    """Удалить пользователя"""
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    """Аутентифицировать пользователя"""
    user = get_user_by_username(db, username)
    if not user:
        return False
    
    if not auth.verify_password(password, user.hashed_password):
        return False
    
    return user


def activate_user(db: Session, user_id: int):
    """Активировать пользователя"""
    user = get_user(db, user_id)
    if user:
        user.is_active = True
        db.commit()
        db.refresh(user)
    return user


def deactivate_user(db: Session, user_id: int):
    """Деактивировать пользователя"""
    user = get_user(db, user_id)
    if user:
        user.is_active = False
        db.commit()
        db.refresh(user)
    return user


def promote_to_admin(db: Session, user_id: int):
    """Назначить пользователя администратором"""
    user = get_user(db, user_id)
    if user:
        user.is_admin = True
        db.commit()
        db.refresh(user)
    return user


def demote_from_admin(db: Session, user_id: int):
    """Лишить пользователя прав администратора"""
    user = get_user(db, user_id)
    if user:
        user.is_admin = False
        db.commit()
        db.refresh(user)
    return user


def update_user_permissions(db: Session, user_id: int, permissions: dict):
    """Обновить права доступа пользователя"""
    user = get_user(db, user_id)
    if user:
        user.permissions = str(permissions)  # Сохраняем как строку JSON
        db.commit()
        db.refresh(user)
    return user