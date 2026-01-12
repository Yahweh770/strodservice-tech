"""
Скрипт для инициализации базы данных и заполнения начальными данными
"""
import os
import sys
from pathlib import Path

# Добавим путь к директории проекта
sys.path.append(str(Path(__file__).parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import DocumentType
from app.crud import create_document_type
from app.schemas import DocumentTypeCreate

# Получаем URL базы данных из переменных окружения, если доступно
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./strod_service_tech.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_database():
    """Инициализация базы данных"""
    print("Создание таблиц в базе данных...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы успешно.")
    
    # Создаем сессию
    db = SessionLocal()
    
    try:
        # Проверим, есть ли уже какие-то типы документов
        existing_types = db.query(DocumentType).count()
        if existing_types == 0:
            # Создаем стандартные типы документов для исполнительной документации
            default_doc_types = [
                {"name": "Исполнительный чертеж", "description": "Чертеж с внесенными изменениями по факту выполнения работ"},
                {"name": "Акт скрытых работ", "description": "Документ, подтверждающий выполнение скрытых работ"},
                {"name": "Журнал производства работ", "description": "Ежедневная регистрация выполненных работ"},
                {"name": "Ведомость объемов работ", "description": "Сводная таблица выполненных объемов"},
                {"name": "Исполнительная съемка", "description": "Геодезическая съемка по факту выполнения работ"},
                {"name": "Протокол испытаний", "description": "Документ с результатами испытаний оборудования/материалов"},
                {"name": "Дефектная ведомость", "description": "Перечень выявленных дефектов и недостатков"},
                {"name": "Акт приемки", "description": "Документ о приемке выполненных работ заказчиком"},
                {"name": "Фотоотчет", "description": "Материалы фотодокументирования выполненных работ"},
                {"name": "Прочая документация", "description": "Другие виды исполнительной документации"}
            ]
            
            print("Добавление стандартных типов документов...")
            for doc_type_data in default_doc_types:
                doc_type = DocumentTypeCreate(**doc_type_data)
                create_document_type(db, doc_type)
            
            print(f"Добавлено {len(default_doc_types)} типов документов.")
        else:
            print(f"База данных уже содержит {existing_types} типов документов, пропускаем инициализацию.")
    
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
    print("Инициализация базы данных завершена.")