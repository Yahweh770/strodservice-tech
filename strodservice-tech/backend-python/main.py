from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

app = FastAPI(title="Строд-Сервис Технолоджи - Python Backend", version="1.0.0")

# Модели данных
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    contract_date: Optional[datetime] = None
    asphalt_laying_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class Project(ProjectBase):
    id: uuid.UUID
    status: str

class Material(BaseModel):
    id: uuid.UUID
    name: str
    batch_number: Optional[str] = None
    manufacturing_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    quantity: float
    unit: str

@app.get("/")
def read_root():
    return {"message": "Строд-Сервис Технолоджи API"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

# Заглушка для основных маршрутов
@app.get("/projects")
def get_projects():
    return {"message": "Список проектов"}

@app.post("/projects")
def create_project(project: ProjectBase):
    return {"message": "Проект создан", "project_name": project.name}

@app.get("/materials")
def get_materials():
    return {"message": "Список материалов"}