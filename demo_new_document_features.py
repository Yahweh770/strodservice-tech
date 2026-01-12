"""
Демонстрационный скрипт для новой функциональности учета документов
"""
import sqlite3
from datetime import datetime
import os

# Путь к базе данных
db_path = "/workspace/src/backend-python/strod_service_tech.db"

def demonstrate_document_system():
    print("=== Демонстрация новой системы учета документов ===\n")
    
    # Подключение к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Проверим, существуют ли нужные таблицы
    tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor.execute(tables_query)
    tables = [row[0] for row in cursor.fetchall()]
    
    print("Существующие таблицы в базе данных:")
    for table in tables:
        print(f"  - {table}")
    
    # Проверим наличие новых таблиц
    new_tables = ['document_types', 'documents', 'document_shipments', 'document_returns']
    missing_tables = [table for table in new_tables if table not in tables]
    
    if missing_tables:
        print(f"\nОтсутствующие таблицы: {missing_tables}")
        print("Выполняем создание таблиц через SQLAlchemy...")
        
        # Импортируем и создаем таблицы
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent / "src/backend-python"))
        
        from sqlalchemy import create_engine
        from app.database import Base
        from app.models import DocumentType, Document, DocumentShipment, DocumentReturn
        
        engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(bind=engine)
        
        print("Таблицы успешно созданы!")
    else:
        print(f"\nВсе новые таблицы ({', '.join(new_tables)}) уже существуют в базе данных.")
    
    # Добавим несколько типов документов, если их нет
    cursor.execute("SELECT COUNT(*) FROM document_types")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("\nДобавляем стандартные типы документов...")
        default_doc_types = [
            ("Исполнительный чертеж", "Чертеж с внесенными изменениями по факту выполнения работ"),
            ("Акт скрытых работ", "Документ, подтверждающий выполнение скрытых работ"),
            ("Журнал производства работ", "Ежедневная регистрация выполненных работ"),
            ("Ведомость объемов работ", "Сводная таблица выполненных объемов"),
            ("Исполнительная съемка", "Геодезическая съемка по факту выполнения работ")
        ]
        
        cursor.executemany(
            "INSERT INTO document_types (name, description, created_at) VALUES (?, ?, ?)",
            [(name, desc, datetime.now().isoformat()) for name, desc in default_doc_types]
        )
        conn.commit()
        print(f"Добавлено {len(default_doc_types)} типов документов.")
    else:
        print(f"\nВ базе данных уже содержится {count} типов документов.")
    
    # Добавим тестовый документ
    cursor.execute("SELECT id FROM document_types LIMIT 1")
    type_id = cursor.fetchone()
    
    if type_id:
        type_id = type_id[0]
        
        # Проверим, есть ли уже документы
        cursor.execute("SELECT COUNT(*) FROM documents")
        doc_count = cursor.fetchone()[0]
        
        if doc_count == 0:
            print("\nДобавляем тестовый документ...")
            cursor.execute("""
                INSERT INTO documents 
                (doc_number, title, project_id, document_type_id, status, created_at) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("DOC-001", "Тестовый исполнительный чертеж", "PROJ-001", type_id, "in_office", datetime.now().isoformat()))
            
            doc_id = cursor.lastrowid
            conn.commit()
            print(f"Добавлен документ с ID: {doc_id}")
        else:
            cursor.execute("SELECT id FROM documents LIMIT 1")
            doc_id = cursor.fetchone()[0]
            print(f"\nИспользуем существующий документ с ID: {doc_id}")
    
    # Проверим структуру таблицы документов
    print("\nСтруктура таблицы 'documents':")
    cursor.execute("PRAGMA table_info(documents)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[1]} ({col[2]}) [{'' if col[5] == 0 else 'PK'}]")
    
    # Проверим структуру таблицы отправок
    print("\nСтруктура таблицы 'document_shipments':")
    cursor.execute("PRAGMA table_info(document_shipments)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[1]} ({col[2]}) [{'' if col[5] == 0 else 'PK'}]")
    
    # Проверим структуру таблицы возвратов
    print("\nСтруктура таблицы 'document_returns':")
    cursor.execute("PRAGMA table_info(document_returns)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[1]} ({col[2]}) [{'' if col[5] == 0 else 'PK'}]")
    
    # Показать примеры данных
    print("\nПримеры типов документов:")
    cursor.execute("SELECT id, name, description FROM document_types LIMIT 5")
    for row in cursor.fetchall():
        print(f"  ID: {row[0]}, Название: {row[1]}, Описание: {row[2]}")
    
    print("\nПримеры документов:")
    cursor.execute("""
        SELECT d.id, d.doc_number, d.title, dt.name as type_name, d.status 
        FROM documents d 
        JOIN document_types dt ON d.document_type_id = dt.id 
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  ID: {row[0]}, №: {row[1]}, Название: {row[2]}, Тип: {row[3]}, Статус: {row[4]}")
    
    conn.close()
    
    print("\n=== Демонстрация завершена ===")
    print("\nНовая система учета документов включает в себя:")
    print("- Таблица 'document_types': Хранит типы документов")
    print("- Таблица 'documents': Хранит информацию о документах")
    print("- Таблица 'document_shipments': Хранит информацию об отправках")
    print("- Таблица 'document_returns': Хранит информацию о возвратах")
    print("\nКаждый документ имеет статус: 'in_office' (в наличии), 'shipped' (отправлен), 'returned' (возвращен)")
    print("Система позволяет отслеживать полный жизненный цикл документа!")

if __name__ == "__main__":
    demonstrate_document_system()