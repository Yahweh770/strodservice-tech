"""
Main module for the Strod-Service backend application.
This module defines the FastAPI application and its routes.
"""
from contextlib import asynccontextmanager
from datetime import date

from fastapi import FastAPI, Request, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api import gpr_routes
from app.api.auth_routes import router as auth_router
from app.api.construction_remarks_routes import router as construction_remarks_router
from app.api.document_routes import router as document_router
from app.api.file_routes import router as file_router
from app.api.work_session_routes import router as work_session_router
from app.auth import get_current_active_user
from app.database import get_db
from app import crud_work_session
from app.websocket_manager import manager
from app.auth import verify_access_token
import json

# Initialize templates
templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запуск инициализации складских остатков при старте приложения
    from app.utils.material_checker import initialize_material_stocks
    from app.database import SessionLocal
    from app import crud_user, schemas
    import os

    db = SessionLocal()
    try:
        initialize_material_stocks(db)

        # Создание администратора по умолчанию при запуске приложения
        admin_username = os.getenv("ADMIN_USERNAME", "Yahweh")
        admin_password = os.getenv("ADMIN_PASSWORD", "90vopepi")

        # Проверяем, существует ли уже администратор с таким именем
        existing_admin = crud_user.get_user_by_username(db, admin_username)
        if not existing_admin:
            # Создаем администратора с правами
            admin_user = schemas.UserCreate(
                username=admin_username,
                email="admin@strod-service.ru",
                full_name="System Administrator",
                position="Administrator",
                department="IT",
                password=admin_password,
                is_active=True,
                is_admin=True,
                permissions={"admin": True, "manage_users": True, "manage_documents": True, "manage_materials": True}
            )

            try:
                created_admin = crud_user.create_user(db, admin_user)
                print(f"Создан администратор: {created_admin.username}")
            except Exception as e:  # pylint: disable=broad-except
                print(f"Ошибка при создании администратора: {e}")
        else:
            print(f"Администратор {existing_admin.username} уже существует")
    finally:
        db.close()
    yield
    # Здесь можно добавить код для завершения работы приложения


app = FastAPI(
    title="Строд-Сервис Технолоджи - Python Backend",
    version="1.0.0",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов ГПР
app.include_router(gpr_routes.router)

# Подключение маршрутов документов
app.include_router(document_router)

# Подключение маршрутов файлов и материалов
app.include_router(file_router)

# Подключение маршрутов аутентификации
app.include_router(auth_router)

# Подключение маршрутов рабочих сессий
app.include_router(work_session_router)

# Подключение маршрутов замечаний от строительного контроля
app.include_router(construction_remarks_router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# WebSocket routes
@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    """WebSocket endpoint для реал-тайм уведомлений"""
    try:
        # Верифицируем токен
        payload = verify_access_token(token)
        user_id = payload.get("user_id")
        
        if not user_id:
            await websocket.close(code=1008, reason="Invalid token")
            return
            
        # Подключаем пользователя к вебсокету
        await manager.connect(websocket, user_id)
        
        try:
            # Отправляем подтверждение подключения
            await manager.send_personal_message(
                json.dumps({"type": "connection", "message": "Connected to server", "user_id": user_id}),
                websocket
            )
            
            # Основной цикл обработки сообщений
            while True:
                # Получаем сообщение от клиента (опционально)
                data = await websocket.receive_text()
                
                # Парсим сообщение
                try:
                    message_data = json.loads(data)
                    message_type = message_data.get("type")
                    
                    # В зависимости от типа сообщения, можем обрабатывать по-разному
                    if message_type == "ping":
                        await manager.send_personal_message(
                            json.dumps({"type": "pong", "message": "Pong"}),
                            websocket
                        )
                    elif message_type == "request_user_info":
                        await manager.send_personal_message(
                            json.dumps({
                                "type": "user_info", 
                                "user_id": user_id,
                                "connections_count": manager.get_user_connections_count(user_id)
                            }),
                            websocket
                        )
                        
                except json.JSONDecodeError:
                    # Если не удалось распарсить JSON, просто продолжаем
                    continue
                    
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            
    except Exception as e:
        await websocket.close(code=1008, reason="Authentication failed")


# Web UI routes

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    # Get current work status
    work_status = crud_work_session.get_current_work_status(db, current_user.id)
    today_sessions = crud_work_session.get_work_sessions_for_date(db, current_user.id, date.today())
    today_hours = crud_work_session.calculate_total_work_hours(today_sessions)

    # Calculate durations for each session
    sessions_with_duration = []
    for session in today_sessions:
        duration = crud_work_session.calculate_work_hours_for_session(session)
        sessions_with_duration.append({
            'session': session,
            'duration': duration
        })

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": current_user,
        "work_status": work_status,
        "today_hours": today_hours,
        "today_sessions": sessions_with_duration
    })


@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, current_user=Depends(get_current_active_user)):
    return templates.TemplateResponse("profile.html", {"request": request, "user": current_user})


@app.get("/employees", response_class=HTMLResponse)
async def employees(request: Request, current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Доступ разрешен только администраторам")

    employees = crud_work_session.get_all_employees_with_work_info(db)
    return templates.TemplateResponse("employees.html", {
        "request": request,
        "user": current_user,
        "employees": employees
    })
