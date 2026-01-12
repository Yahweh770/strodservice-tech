from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import gpr_routes
from app.api.document_routes import router as document_router
from app.api.file_routes import router as file_router
from app.api.auth_routes import router as auth_router

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
            except Exception as e:
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

@app.get("/")
def read_root():
    return {"message": "Строд-Сервис Технолоджи API - Управление строительством"}