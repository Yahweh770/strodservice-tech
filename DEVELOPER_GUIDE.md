# Руководство по адаптации приложения для командного использования

## Обзор

Это руководство содержит пошаговые инструкции по преобразованию однопользовательской десктопной версии "Строд-Сервис Технолоджи" в многопользовательскую веб-систему.

## 1. Архитектурные изменения

### 1.1. Переход к веб-серверной архитектуре

#### Текущая архитектура:
- Electron-приложение запускает Python-сервер локально
- Frontend и Backend связаны в одном приложении
- Данные хранятся в локальной SQLite базе

#### Целевая архитектура:
- Независимый Backend-сервер (FastAPI) на отдельном хосте
- Frontend-приложение подключается к серверу по API
- Поддержка подключения множества клиентов к одному серверу

#### Изменения в electron-main.js:
```javascript
// Добавить возможность подключения к удаленному серверу
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

ipcMain.handle('send-request', async (event, method, endpoint, data) => {
  try {
    const response = await axios({
      method: method,
      url: `${BACKEND_URL}${endpoint}`,  // Использовать настраиваемый URL
      data: data,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${currentUserToken}`  // Добавить токен авторизации
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Error sending request to backend:', error.message);
    throw error;
  }
});
```

### 1.2. Поддержка многопользовательского режима

#### Обновление модели пользователя (app/models/user.py):
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    position = Column(String, nullable=True)  # Должность
    department = Column(String, nullable=True)  # Отдел
    company_id = Column(Integer, nullable=True)  # ID компании (для мультитенантности)
    is_active = Column(Boolean, default=True, index=True)
    is_admin = Column(Boolean, default=False, index=True)
    role = Column(String, default="user")  # Роль пользователя
    permissions = Column(Text, default='{}')  # JSON строка с правами
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
```

## 2. Обновление системы аутентификации

### 2.1. Добавление ролевой модели

#### В auth.py:
```python
from enum import Enum
from typing import Dict, List

class UserRole(str, Enum):
    ADMIN = "admin"
    PROJECT_MANAGER = "project_manager"
    ENGINEER_PTO = "engineer_pto"
    SUPERVISOR = "supervisor"
    MATERIAL_SPECIALIST = "material_specialist"
    USER = "user"

def check_permission(user, resource_type: str, action: str) -> bool:
    """
    Проверка прав доступа пользователя к ресурсу
    """
    permissions = json.loads(user.permissions)
    
    # Проверка глобальных прав
    if user.is_admin or permissions.get('admin', False):
        return True
        
    # Проверка прав на уровне ресурса
    resource_perms = permissions.get(resource_type, {})
    return resource_perms.get(action, False)

def get_accessible_projects(user, db_session):
    """
    Получение списка проектов, к которым у пользователя есть доступ
    """
    # Если админ - доступ ко всем проектам
    if user.is_admin:
        return db_session.query(Project).all()
    
    # Иначе - только к назначенным проектам
    return db_session.query(Project).join(ProjectAccess).filter(
        ProjectAccess.user_id == user.id
    ).all()
```

### 2.2. Обновление маршрутов аутентификации

#### В api/auth_routes.py:
```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import json

from .. import crud_user, schemas
from ..database import get_db
from ..auth import (
    authenticate_user, 
    create_access_token, 
    create_refresh_token,
    get_current_active_user
)

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Обновить время последнего входа
    user.last_login = datetime.utcnow()
    db.commit()
    
    access_token_expires = timedelta(minutes=30)
    refresh_token_expires = timedelta(days=7)
    
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=refresh_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "user_info": {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "position": user.position,
            "department": user.department,
            "role": user.role,
            "permissions": json.loads(user.permissions)
        }
    }

@router.post("/register")
async def register_user(
    user_data: schemas.UserCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Только администраторы могут регистрировать новых пользователей
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Only administrators can register new users"
        )
    
    # Проверить, существует ли пользователь
    existing_user = crud_user.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Создать нового пользователя
    user = crud_user.create_user(db, user_data)
    return {"message": "User created successfully", "user_id": user.id}
```

## 3. Переход на PostgreSQL

### 3.1. Обновление конфигурации базы данных

#### В database.py:
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Поддержка различных типов баз данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./strod_service_tech.db")

if "postgresql" in DATABASE_URL.lower():
    # Настройки для PostgreSQL в многопользовательской среде
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,
        max_overflow=30,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False
    )
elif "mysql" in DATABASE_URL.lower():
    engine = create_engine(
        DATABASE_URL,
        pool_size=15,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False
    )
else:
    # Для SQLite (в основном для разработки)
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### 3.2. Обновление моделей для поддержки многопользовательского доступа

#### Добавление связей с пользователями в существующие модели:
```python
# В app/models/gpr.py
class GPR(Base):
    __tablename__ = "gpr"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))  # Кто создал
    assigned_to = Column(Integer, ForeignKey("users.id"))  # Кто ответственный
    data = Column(Text)  # JSON данные графика
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связи
    creator = relationship("User", foreign_keys=[created_by])
    assignee = relationship("User", foreign_keys=[assigned_to])
    project = relationship("Project")
```

## 4. Обновление API маршрутов

### 4.1. Добавление проверки прав доступа к ресурсам

#### В api/gpr_routes.py:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..auth import get_current_active_user
from ..utils.permissions import check_resource_access

router = APIRouter()

@router.get("/", response_model=list[schemas.GPR])
def read_gpr_list(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Получить только те ГПР, к которым у пользователя есть доступ
    gpr_list = crud.get_gpr_list_for_user(db, current_user, skip=skip, limit=limit)
    return gpr_list

@router.post("/", response_model=schemas.GPR)
def create_gpr(
    gpr: schemas.GPRCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Проверить, есть ли у пользователя право создавать ГПР для указанного проекта
    if not check_resource_access(current_user, gpr.project_id, "create_gpr"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Установить создателя
    gpr.created_by = current_user.id
    return crud.create_gpr(db=db, gpr=gpr, user_id=current_user.id)

@router.get("/{gpr_id}", response_model=schemas.GPR)
def read_gpr(
    gpr_id: int,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    gpr = crud.get_gpr(db, gpr_id=gpr_id)
    if gpr is None:
        raise HTTPException(status_code=404, detail="GPR not found")
    
    # Проверить доступ к конкретному ГПР
    if not check_resource_access(current_user, gpr.project_id, "read"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return gpr
```

## 5. Реализация синхронизации данных

### 5.1. Добавление WebSocket для уведомлений

#### В main.py:
```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}  # user_id -> websocket

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: int):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_text(message)

    async def broadcast_to_project_users(self, message: str, project_id: int, exclude_user: int = None):
        # Отправить сообщение всем пользователям, имеющим доступ к проекту
        connected_users = [uid for uid in self.active_connections.keys()]
        
        for user_id in connected_users:
            if user_id != exclude_user and check_user_project_access(user_id, project_id):
                await self.send_personal_message(message, user_id)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, token: str):
    # Проверить токен и права доступа
    if not validate_websocket_token(token, user_id):
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Обработать входящее сообщение
            message_data = json.loads(data)
            
            # В зависимости от типа сообщения выполнить соответствующее действие
            if message_data.get("type") == "ping":
                await manager.send_personal_message('{"type": "pong"}', user_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
```

## 6. Безопасность

### 6.1. Добавление middleware для аудита

#### В main.py:
```python
from fastapi import Request
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Логирование входящих запросов
    logger.info(f"{request.method} {request.url} - {request.client.host}")
    
    response = await call_next(request)
    
    # Логирование результатов
    logger.info(f"{request.method} {request.url} - {response.status_code}")
    
    return response

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```

## 7. Миграция данных

### 7.1. Создание скрипта миграции

#### Файл: migrate_to_postgres.py
```python
"""
Скрипт для миграции данных из SQLite в PostgreSQL
"""
import sqlite3
import psycopg2
import json
from datetime import datetime

def migrate_users(sqlite_conn, pg_conn):
    """Миграция пользователей"""
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    # Получить пользователей из SQLite
    sqlite_cursor.execute("SELECT * FROM users")
    users = sqlite_cursor.fetchall()
    
    for user in users:
        # Вставить в PostgreSQL
        pg_cursor.execute("""
            INSERT INTO users (id, username, email, hashed_password, full_name, 
                            position, department, is_active, is_admin, permissions, 
                            created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING
        """, user)
    
    pg_conn.commit()

def main():
    # Подключение к SQLite
    sqlite_conn = sqlite3.connect("strod_service_tech.db")
    
    # Подключение к PostgreSQL
    pg_conn = psycopg2.connect(
        host="localhost",
        database="strod_service_db",
        user="strod_user",
        password="secure_password"
    )
    
    try:
        # Миграция всех таблиц
        migrate_users(sqlite_conn, pg_conn)
        # Добавить другие функции миграции...
        
        print("Миграция данных успешно завершена!")
    except Exception as e:
        print(f"Ошибка при миграции: {e}")
        pg_conn.rollback()
    finally:
        sqlite_conn.close()
        pg_conn.close()

if __name__ == "__main__":
    main()
```

## 8. Тестирование

### 8.1. Создание тестов для многопользовательской функциональности

#### Файл: test_multiuser.py
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture
def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()

def test_user_authentication():
    """Тест аутентификации пользователя"""
    response = client.post("/auth/login", data={
        "username": "test_user",
        "password": "test_password"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_project_access_control():
    """Тест контроля доступа к проектам"""
    # Аутентифицировать пользователя
    auth_response = client.post("/auth/login", data={
        "username": "limited_user",
        "password": "password"
    })
    token = auth_response.json()["access_token"]
    
    # Попытаться получить доступ к проекту
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/projects/1", headers=headers)
    
    # Ожидаем 403 если нет доступа или 200 если есть
    assert response.status_code in [200, 403]
```

## Заключение

Это руководство охватывает основные изменения, необходимые для преобразования однопользовательского приложения в многопользовательскую систему. Ключевые аспекты:

1. Архитектурные изменения для поддержки веб-сервера
2. Расширенная система аутентификации и авторизации
3. Переход на PostgreSQL для поддержки конкурентного доступа
4. Реализация контроля доступа к ресурсам
5. Добавление синхронизации данных через WebSocket
6. Обеспечение безопасности в многопользовательской среде

При реализации этих изменений важно проводить тестирование на каждом этапе и обеспечивать обратную совместимость с существующими данными.