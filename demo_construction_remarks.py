#!/usr/bin/env python3
"""
Демонстрационный скрипт для системы замечаний от строительного контроля
"""

import os
import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Добавляем путь к backend
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'backend-python'))

from app.database import SessionLocal, engine
from app import models, schemas, crud, crud_construction_remarks


def demo_construction_remarks():
    """Демонстрация работы системы замечаний от строительного контроля"""
    print("=== Демонстрация системы замечаний от строительного контроля ===\n")
    
    # Создаем сессию базы данных
    db = SessionLocal()
    
    try:
        # Создаем тестовый объект проекта, если его нет
        test_objects = crud.get_project_objects(db, skip=0, limit=1)
        if not test_objects:
            project_object = schemas.ProjectObjectCreate(
                object_id="OBJ-001",
                name="Тестовый объект строительства",
                location="г. Москва, ул. Тестовая, д. 1",
                description="Тестовый объект для демонстрации системы замечаний"
            )
            project_obj = crud.create_project_object(db, project_object)
            print(f"Создан тестовый объект проекта: {project_obj.name}")
        else:
            project_obj = test_objects[0]
            print(f"Используем существующий объект проекта: {project_obj.name}")
        
        print()
        
        # Создаем новое замечание
        print("1. Создание нового замечания...")
        remark_create = schemas.ConstructionRemarkCreate(
            remark_number="REM-001",
            project_object_id=project_obj.id,
            title="Нарушение технологии укладки бетона",
            description="Обнаружено нарушение технологии укладки бетона в зоне фундамента. Бетон уложен с нарушением требований СНиП.",
            status=schemas.RemarkStatus.NEW,
            priority="high",
            assigned_to="Иванов И.И.",
            deadline=datetime.now() + timedelta(days=7),
            created_by="Строительный контроль"
        )
        
        new_remark = crud_construction_remarks.create_construction_remark(db, remark_create)
        print(f"   Создано замечание: {new_remark.title}")
        print(f"   Номер: {new_remark.remark_number}")
        print(f"   Статус: {new_remark.status}")
        print(f"   Приоритет: {new_remark.priority}")
        print(f"   Назначено: {new_remark.assigned_to}")
        print(f"   Срок: {new_remark.deadline}")
        print()
        
        # Обновляем статус замечания
        print("2. Обновление статуса замечания...")
        remark_update = schemas.ConstructionRemarkUpdate(
            status=schemas.RemarkStatus.IN_PROGRESS,
            assigned_to="Петров П.П."
        )
        updated_remark = crud_construction_remarks.update_construction_remark(db, new_remark.id, remark_update)
        print(f"   Статус изменен на: {updated_remark.status}")
        print(f"   Назначено: {updated_remark.assigned_to}")
        print()
        
        # Получаем историю изменений
        print("3. Получение истории изменений...")
        history = crud_construction_remarks.get_remark_history(db, new_remark.id)
        for h in history:
            print(f"   {h.changed_at}: {h.old_status} -> {h.new_status} (кем: {h.changed_by})")
        print()
        
        # Создаем тестовую фотографию (виртуально)
        print("4. Добавление фотографии к замечанию...")
        # В реальной системе здесь будет загрузка файла, мы создадим виртуальную запись
        photo_create = schemas.RemarkPhotoCreate(
            remark_id=new_remark.id,
            file_path="/uploads/remark_photos/test_photo.jpg",
            filename="test_photo.jpg",
            file_size=1024000,  # 1MB
            description="Фото нарушения технологии укладки бетона",
            created_by="Строительный контроль"
        )
        photo = crud_construction_remarks.create_remark_photo(db, photo_create)
        print(f"   Добавлена фотография: {photo.filename}")
        print(f"   Описание: {photo.description}")
        print()
        
        # Получаем все фотографии для замечания
        print("5. Получение всех фотографий для замечания...")
        photos = crud_construction_remarks.get_remark_photos(db, new_remark.id)
        for p in photos:
            print(f"   Фото: {p.filename} ({p.file_size} bytes)")
        print()
        
        # Получаем все замечания для объекта проекта
        print("6. Получение всех замечаний для объекта проекта...")
        remarks = crud_construction_remarks.get_remarks_by_project_object(db, project_obj.id)
        for r in remarks:
            print(f"   {r.remark_number}: {r.title} - {r.status}")
        print()
        
        # Получаем сводку по замечаниям для объекта
        print("7. Получение сводки по замечаниям для объекта...")
        summary = crud_construction_remarks.get_remarks_summary_by_project_object(db, project_obj.id)
        print(f"   Всего замечаний: {summary['total']}")
        print(f"   По статусам: {summary['by_status']}")
        print()
        
        # Поиск замечаний
        print("8. Поиск замечаний по ключевому слову...")
        search_results = crud_construction_remarks.search_construction_remarks(db, query_str="бетона")
        for r in search_results:
            print(f"   Найдено: {r.remark_number} - {r.title}")
        print()
        
        # Получаем все замечания с определенным статусом
        print("9. Получение всех замечаний со статусом 'в работе'...")
        in_progress_remarks = crud_construction_remarks.get_remarks_by_status(db, schemas.RemarkStatus.IN_PROGRESS)
        for r in in_progress_remarks:
            print(f"   {r.remark_number}: {r.title} - {r.status}")
        print()
        
        # Проверяем наличие просроченных замечаний
        print("10. Проверка наличия просроченных замечаний...")
        overdue_remarks = crud_construction_remarks.get_overdue_remarks(db)
        if overdue_remarks:
            for r in overdue_remarks:
                print(f"   Просрочено: {r.remark_number} - {r.title}")
        else:
            print("   Нет просроченных замечаний")
        print()
        
        # Полное получение замечания с деталями
        print("11. Полное получение замечания с деталями...")
        full_remark = crud_construction_remarks.get_construction_remark(db, new_remark.id)
        if full_remark:
            full_remark.photos = crud_construction_remarks.get_remark_photos(db, new_remark.id)
            full_remark.history = crud_construction_remarks.get_remark_history(db, new_remark.id)
            
            print(f"   Замечание: {full_remark.title}")
            print(f"   Фотографий: {len(full_remark.photos)}")
            print(f"   Записей в истории: {len(full_remark.history)}")
        
    except Exception as e:
        print(f"Ошибка при выполнении демонстрации: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    demo_construction_remarks()