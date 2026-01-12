from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta
import json

from .. import crud, crud_user, auth, schemas, database
from ..auth import get_current_user as get_current_user_auth

router = APIRouter(prefix="/auth", tags=["authentication"])

security = HTTPBearer()


@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Регистрация нового пользователя"""
    try:
        db_user = crud_user.create_user(db, user)
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=schemas.Token)
def login_user(login_data: schemas.UserLogin, db: Session = Depends(database.get_db)):
    """Вход пользователя в систему"""
    user = crud_user.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Аккаунт пользователя деактивирован",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Пытаемся преобразовать permissions из строки обратно в словарь
    permissions_dict = {}
    try:
        permissions_dict = json.loads(user.permissions) if user.permissions else {}
    except (json.JSONDecodeError, TypeError):
        # Если не получается распарсить, используем пустой словарь
        permissions_dict = {}
    
    # Создаем JWT токен
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id,
            "is_admin": user.is_admin,
            "permissions": permissions_dict
        },
        expires_delta=access_token_expires
    )
    
    token_data = schemas.Token(
        access_token=access_token,
        token_type="bearer",
        user=schemas.UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            position=user.position,
            department=user.department,
            is_active=user.is_active,
            is_admin=user.is_admin,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    )
    
    return token_data


@router.post("/logout")
def logout_user(current_user: dict = Depends(get_current_user_auth)):
    """Выход пользователя из системы"""
    # В реальной реализации здесь может быть инвалидация токена
    return {"message": f"Пользователь {current_user['username']} успешно вышел из системы"}


@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: dict = Depends(get_current_user_auth)):
    """Получить информацию о текущем пользователе"""
    # Получаем полную информацию о пользователе из базы данных
    db = database.SessionLocal()
    try:
        user = crud_user.get_user(db, current_user["user_id"])
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        return schemas.UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            position=user.position,
            department=user.department,
            is_active=user.is_active,
            is_admin=user.is_admin,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    finally:
        db.close()


@router.put("/me", response_model=schemas.UserResponse)
def update_my_profile(
    user_update: schemas.UserUpdate,
    current_user: dict = Depends(get_current_user_auth),
    db: Session = Depends(database.get_db)
):
    """Обновить собственный профиль"""
    user = crud_user.get_user(db, current_user["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Обновляем только разрешенные поля (без is_admin, is_active и других системных)
    allowed_fields = ["email", "full_name", "position", "department"]
    update_data = user_update.model_dump(exclude_unset=True)
    
    filtered_update = {}
    for field, value in update_data.items():
        if field in allowed_fields:
            filtered_update[field] = value
    
    # Создаем временный объект для обновления только нужных полей
    temp_update = schemas.UserUpdate(**filtered_update)
    
    updated_user = crud_user.update_user(db, current_user["user_id"], temp_update)
    return updated_user


@router.get("/users", response_model=list[schemas.UserResponse])
def read_users(
    skip: int = 0, 
    limit: int = 100,
    current_user: dict = Depends(get_current_user_auth),
    db: Session = Depends(database.get_db)
):
    """Получить список всех пользователей (только для администраторов)"""
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для просмотра списка пользователей"
        )
    
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return [
        schemas.UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            position=user.position,
            department=user.department,
            is_active=user.is_active,
            is_admin=user.is_admin,
            created_at=user.created_at,
            updated_at=user.updated_at
        ) for user in users
    ]


@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(
    user_id: int,
    current_user: dict = Depends(get_current_user_auth),
    db: Session = Depends(database.get_db)
):
    """Получить информацию о конкретном пользователе (только для администраторов)"""
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для просмотра информации о пользователе"
        )
    
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return schemas.UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        position=user.position,
        department=user.department,
        is_active=user.is_active,
        is_admin=user.is_admin,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    current_user: dict = Depends(get_current_user_auth),
    db: Session = Depends(database.get_db)
):
    """Обновить информацию о пользователе (только для администраторов)"""
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для изменения информации о пользователе"
        )
    
    # Проверяем, что пользователь существует
    existing_user = crud_user.get_user(db, user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    updated_user = crud_user.update_user(db, user_id, user_update)
    return updated_user


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: dict = Depends(get_current_user_auth),
    db: Session = Depends(database.get_db)
):
    """Удалить пользователя (только для администраторов)"""
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для удаления пользователя"
        )
    
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if user.is_admin and user.id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя удалить другого администратора"
        )
    
    crud_user.delete_user(db, user_id)
    return {"message": f"Пользователь {user.username} успешно удален"}


@router.post("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    current_user: dict = Depends(get_current_user_auth),
    db: Session = Depends(database.get_db)
):
    """Активировать пользователя (только для администраторов)"""
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для активации пользователя"
        )
    
    user = crud_user.activate_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return {"message": f"Пользователь {user.username} успешно активирован"}


@router.post("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    current_user: dict = Depends(get_current_user_auth),
    db: Session = Depends(database.get_db)
):
    """Деактивировать пользователя (только для администраторов)"""
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для деактивации пользователя"
        )
    
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if user.is_admin and user.id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя деактивировать другого администратора"
        )
    
    deactivated_user = crud_user.deactivate_user(db, user_id)
    return {"message": f"Пользователь {deactivated_user.username} успешно деактивирован"}


@router.post("/users/{user_id}/promote-admin")
def promote_to_admin(
    user_id: int,
    current_user: dict = Depends(get_current_user_auth),
    db: Session = Depends(database.get_db)
):
    """Назначить пользователя администратором (только для администраторов)"""
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для назначения администратора"
        )
    
    # Проверяем, что текущий пользователь - администратор
    admin_user = crud_user.get_user(db, current_user["user_id"])
    if not admin_user or not admin_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администраторы могут назначать других администраторов"
        )
    
    user = crud_user.promote_to_admin(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return {"message": f"Пользователь {user.username} назначен администратором"}


@router.post("/users/{user_id}/demote-admin")
def demote_from_admin(
    user_id: int,
    current_user: dict = Depends(get_current_user_auth),
    db: Session = Depends(database.get_db)
):
    """Лишить пользователя прав администратора (только для администраторов)"""
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для лишения прав администратора"
        )
    
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if user.id == current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя лишить себя прав администратора"
        )
    
    demoted_user = crud_user.demote_from_admin(db, user_id)
    return {"message": f"У пользователя {demoted_user.username} отобраны права администратора"}


@router.put("/users/{user_id}/permissions")
def update_user_permissions(
    user_id: int,
    permissions: dict,
    current_user: dict = Depends(get_current_user_auth),
    db: Session = Depends(database.get_db)
):
    """Обновить права доступа пользователя (только для администраторов)"""
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для изменения прав доступа"
        )
    
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    updated_user = crud_user.update_user_permissions(db, user_id, permissions)
    return {"message": f"Права доступа пользователя {updated_user.username} обновлены", "user": updated_user}