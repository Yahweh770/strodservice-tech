"""
Тестовый скрипт для проверки API документов
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_document_api():
    """Тестирование API документов"""
    print("=== Тестирование API документов ===")
    
    # 1. Получение типов документов
    print("\n1. Получение типов документов:")
    try:
        response = requests.get(f"{BASE_URL}/api/documents/types")
        if response.status_code == 200:
            doc_types = response.json()
            print(f"   Успешно получено {len(doc_types)} типов документов")
            for dt in doc_types[:3]:  # Показываем первые 3
                print(f"   - {dt['name']}: {dt['description']}")
        else:
            print(f"   Ошибка получения типов документов: {response.status_code}")
    except Exception as e:
        print(f"   Ошибка при запросе типов документов: {e}")
    
    # 2. Создание нового типа документа (если нужно)
    print("\n2. Создание нового типа документа:")
    try:
        new_type_data = {
            "name": "Тестовый тип документа",
            "description": "Тип документа для тестирования API"
        }
        response = requests.post(f"{BASE_URL}/api/documents/types", json=new_type_data)
        if response.status_code == 200:
            created_type = response.json()
            print(f"   Успешно создан тип документа: {created_type['name']}")
            type_id = created_type['id']
        else:
            print(f"   Ошибка создания типа документа: {response.status_code}")
            print(f"   Ответ: {response.text}")
    except Exception as e:
        print(f"   Ошибка при создании типа документа: {e}")
    
    # 3. Создание документа
    print("\n3. Создание документа:")
    try:
        # Используем первый доступный тип документа или только что созданный
        doc_data = {
            "doc_number": "TEST-001",
            "title": "Тестовый документ учета",
            "project_id": "PROJ-001",
            "document_type_id": 1  # Используем первый тип
        }
        response = requests.post(f"{BASE_URL}/api/documents/", json=doc_data)
        if response.status_code == 200:
            created_doc = response.json()
            print(f"   Успешно создан документ: {created_doc['title']} (ID: {created_doc['id']})")
            doc_id = created_doc['id']
        else:
            print(f"   Ошибка создания документа: {response.status_code}")
            print(f"   Ответ: {response.text}")
    except Exception as e:
        print(f"   Ошибка при создании документа: {e}")
    
    # 4. Получение списка документов
    print("\n4. Получение списка документов:")
    try:
        response = requests.get(f"{BASE_URL}/api/documents/")
        if response.status_code == 200:
            docs = response.json()
            print(f"   Успешно получено {len(docs)} документов")
            for d in docs[:3]:  # Показываем первые 3
                print(f"   - {d['doc_number']}: {d['title']} (Статус: {d['status']})")
        else:
            print(f"   Ошибка получения документов: {response.status_code}")
    except Exception as e:
        print(f"   Ошибка при запросе документов: {e}")
    
    # 5. Отправка документа (если документ был создан)
    if 'doc_id' in locals():
        print(f"\n5. Отправка документа ID {doc_id}:")
        try:
            shipment_data = {
                "document_id": doc_id,
                "recipient": "Тестовый получатель",
                "shipment_date": datetime.now().isoformat(),
                "notes": "Тестовая отправка документа"
            }
            response = requests.post(f"{BASE_URL}/api/documents/{doc_id}/shipments", json=shipment_data)
            if response.status_code == 200:
                created_shipment = response.json()
                print(f"   Успешно создана отправка: {created_shipment['recipient']}")
            else:
                print(f"   Ошибка создания отправки: {response.status_code}")
                print(f"   Ответ: {response.text}")
        except Exception as e:
            print(f"   Ошибка при отправке документа: {e}")
    
    print("\n=== Тестирование завершено ===")

if __name__ == "__main__":
    print("Проверка доступности API...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("API доступен, запуск тестов...")
            test_document_api()
        else:
            print(f"API недоступен, код состояния: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Не удается подключиться к API. Убедитесь, что сервер запущен на http://localhost:8000")