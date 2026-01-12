#!/usr/bin/env python3
"""
Демонстрационный скрипт для системы учета документов ПТО
"""

from doc_tracking_system import DocTrackingSystem
from datetime import datetime, timedelta

def demo():
    print("=== Демонстрация системы учета документов ПТО ===\n")
    
    # Создаем экземпляр системы
    system = DocTrackingSystem()
    
    # Добавляем несколько тестовых документов
    print("1. Добавление тестовых документов:")
    doc1_id = system.add_document(
        doc_number="ПТО-001",
        doc_title="Исполнительный чертеж конструкции №1",
        project_number="ПРОЕКТ-2023-01",
        issue_date="2023-01-15",
        doc_type="Чертеж"
    )
    
    doc2_id = system.add_document(
        doc_number="ПТО-002",
        doc_title="Спецификация материалов",
        project_number="ПРОЕКТ-2023-01",
        issue_date="2023-01-20",
        doc_type="Спецификация"
    )
    
    doc3_id = system.add_document(
        doc_number="ПТО-003",
        doc_title="Акт осмотра оборудования",
        project_number="ПРОЕКТ-2023-02",
        issue_date="2023-02-01",
        doc_type="Акт"
    )
    
    print()
    
    # Показываем все документы
    print("2. Список всех документов:")
    docs = system.list_documents()
    print(f"{'ID':<5} {'Номер':<15} {'Наименование':<35} {'Проект':<15} {'Статус':<15}")
    print("-" * 90)
    for doc in docs:
        doc_id, doc_number, doc_title, project_number, status, shipment_date, recipient, return_date = doc
        print(f"{doc_id:<5} {doc_number:<15} {doc_title[:34]:<35} {project_number or '':<15} {status:<15}")
    print()
    
    # Отправляем два документа
    print("3. Отправка документов:")
    system.ship_document(doc1_id, "ООО 'Строймонтаж'", "2023-02-10", "Отправлено курьером")
    system.ship_document(doc2_id, "ЗАО 'Проектсервис'", "2023-02-12", "Передано через представителя")
    print()
    
    # Показываем обновленный список
    print("4. Статус после отправки:")
    docs = system.list_documents()
    print(f"{'ID':<5} {'Номер':<15} {'Наименование':<35} {'Проект':<15} {'Статус':<15} {'Отправлен':<12} {'Получатель':<20}")
    print("-" * 115)
    for doc in docs:
        doc_id, doc_number, doc_title, project_number, status, shipment_date, recipient, return_date = doc
        print(f"{doc_id:<5} {doc_number:<15} {doc_title[:34]:<35} {project_number or '':<15} {status:<15} {shipment_date or '':<12} {recipient or '':<20}")
    print()
    
    # Возвращаем один документ
    print("5. Возврат документа:")
    system.return_document(doc1_id, "Хорошее", "Документ подписан и возвращен")
    print()
    
    # Показываем финальный статус
    print("6. Финальный статус документов:")
    docs = system.list_documents()
    print(f"{'ID':<5} {'Номер':<15} {'Наименование':<35} {'Проект':<15} {'Статус':<15} {'Отправлен':<12} {'Получатель':<20} {'Возвращен':<12}")
    print("-" * 130)
    for doc in docs:
        doc_id, doc_number, doc_title, project_number, status, shipment_date, recipient, return_date = doc
        print(f"{doc_id:<5} {doc_number:<15} {doc_title[:34]:<35} {project_number or '':<15} {status:<15} {shipment_date or '':<12} {recipient or '':<20} {return_date or '':<12}")
    print()
    
    # Демонстрация поиска
    print("7. Поиск документов по ключевому слову 'чертеж':")
    found_docs = system.search_documents("чертеж")
    print(f"{'ID':<5} {'Номер':<15} {'Наименование':<35} {'Проект':<15} {'Статус':<15}")
    print("-" * 90)
    for doc in found_docs:
        doc_id, doc_number, doc_title, project_number, status, shipment_date, recipient, return_date = doc
        print(f"{doc_id:<5} {doc_number:<15} {doc_title[:34]:<35} {project_number or '':<15} {status:<15}")
    print()

if __name__ == "__main__":
    demo()