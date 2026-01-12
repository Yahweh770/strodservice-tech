from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


# Базовая схема пользователя
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False
    permissions: Optional[Dict[str, Any]] = {}


# Схема для создания пользователя
class UserCreate(UserBase):
    password: str


# Схема для обновления пользователя
class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    permissions: Optional[Dict[str, Any]] = None


# Схема пользователя для ответа (без пароля)
class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Схема для входа в систему
class UserLogin(BaseModel):
    username: str
    password: str


# Схема ответа токена
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# Схема данных токена
class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    is_admin: Optional[bool] = None
    permissions: Optional[Dict[str, Any]] = {}