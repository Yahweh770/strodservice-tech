from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import gpr_routes
from app.api.document_routes import router as document_router
from app.api.file_routes import router as file_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запуск инициализации складских остатков при старте приложения
    from app.utils.material_checker import initialize_material_stocks
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        initialize_material_stocks(db)
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

@app.get("/")
def read_root():
    return {"message": "Строд-Сервис Технолоджи API - Управление строительством"}