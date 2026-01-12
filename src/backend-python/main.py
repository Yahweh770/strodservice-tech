from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import gpr_routes
from app.api.document_routes import router as document_router

app = FastAPI(title="Строд-Сервис Технолоджи - Python Backend", version="1.0.0")

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

@app.get("/")
def read_root():
    return {"message": "Строд-Сервис Технолоджи API - Управление строительством"}