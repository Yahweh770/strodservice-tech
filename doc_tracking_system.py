#!/usr/bin/env python3
"""
Система учета отправленных и возвращенных документов исполнительной документации в ПТО
"""

import sqlite3
from datetime import datetime

class DocTrackingSystem:
    """Класс системы учета документов"""
    def __init__(self, db_path="pto_docs.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Таблица пользователей для многопользовательского режима
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Таблица документов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_number TEXT NOT NULL,
                doc_title TEXT NOT NULL,
                project_number TEXT,
                issue_date DATE,
                doc_type TEXT,
                status TEXT DEFAULT 'в наличии',
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_by INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id),
                FOREIGN KEY (updated_by) REFERENCES users (id)
            )
        ''')

        # Таблица отправок
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shipments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id INTEGER,
                recipient TEXT NOT NULL,
                shipment_date DATE NOT NULL,
                shipped_by INTEGER,
                notes TEXT,
                FOREIGN KEY (doc_id) REFERENCES documents (id),
                FOREIGN KEY (shipped_by) REFERENCES users (id)
            )
        ''')

        # Таблица возвратов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS returns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id INTEGER,
                return_date DATE NOT NULL,
                returned_by INTEGER,
                condition TEXT,
                notes TEXT,
                FOREIGN KEY (doc_id) REFERENCES documents (id),
                FOREIGN KEY (returned_by) REFERENCES users (id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_document(self, doc_number, doc_title, project_number=None, issue_date=None, doc_type=None, user_id=None):
        """Добавление нового документа"""
        # Валидация входных данных
        if not doc_number or not doc_title:
            print("Ошибка: Номер и наименование документа обязательны")
            return None

        # Проверка формата даты
        if issue_date:
            try:
                datetime.strptime(issue_date, '%Y-%m-%d')
            except ValueError:
                print("Ошибка: Неверный формат даты. Используйте ГГГГ-ММ-ДД")
                return None

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO documents (doc_number, doc_title, project_number, issue_date, doc_type, created_by)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (doc_number, doc_title, project_number, issue_date, doc_type, user_id))

            doc_id = cursor.lastrowid
            conn.commit()

            print(f"Документ '{doc_title}' (ID: {doc_id}) успешно добавлен пользователем {user_id}")
            return doc_id

    def get_document_by_id(self, doc_id):
        """Получение информации о документе по ID"""
        # Проверка корректности ID
        if not isinstance(doc_id, int) or doc_id <= 0:
            print("Ошибка: ID документа должен быть положительным целым числом")
            return None

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM documents WHERE id = ?
            ''', (doc_id,))

            doc = cursor.fetchone()

            return doc

    def list_documents(self):
        """Список всех документов"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Используем подзапросы для получения последней отправки и возврата для каждого документа
        # А также информацию о пользователях
        cursor.execute('''
            SELECT
                d.id,
                d.doc_number,
                d.doc_title,
                d.project_number,
                d.status,
                (SELECT s.shipment_date FROM shipments s WHERE s.doc_id = d.id ORDER BY s.id DESC LIMIT 1) as shipment_date,
                (SELECT s.recipient FROM shipments s WHERE s.doc_id = d.id ORDER BY s.id DESC LIMIT 1) as recipient,
                (SELECT u.full_name FROM shipments s JOIN users u ON s.shipped_by = u.id WHERE s.doc_id = d.id ORDER BY s.id DESC LIMIT 1) as shipped_by_name,
                (SELECT r.return_date FROM returns r WHERE r.doc_id = d.id ORDER BY r.id DESC LIMIT 1) as return_date,
                (SELECT u.full_name FROM returns r JOIN users u ON r.returned_by = u.id WHERE r.doc_id = d.id ORDER BY r.id DESC LIMIT 1) as returned_by_name
            FROM documents d
            ORDER BY d.id
        ''')

        docs = cursor.fetchall()
        conn.close()

        return docs

    def ship_document(self, doc_id, recipient, shipment_date=None, notes=None, user_id=None):
        """Отправка документа"""
        # Валидация параметров
        if not isinstance(doc_id, int) or doc_id <= 0:
            print("Ошибка: ID документа должен быть положительным целым числом")
            return False

        if not recipient or not recipient.strip():
            print("Ошибка: Получатель обязателен")
            return False

        # Проверка формата даты
        if shipment_date:
            try:
                datetime.strptime(shipment_date, '%Y-%m-%d')
            except ValueError:
                print("Ошибка: Неверный формат даты. Используйте ГГГГ-ММ-ДД")
                return False
        else:
            shipment_date = datetime.now().strftime('%Y-%m-%d')

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Проверяем, существует ли документ
            cursor.execute('SELECT id, status FROM documents WHERE id = ?', (doc_id,))
            doc = cursor.fetchone()
            if not doc:
                print(f"Документ с ID {doc_id} не найден")
                return False

            # Проверяем статус документа
            if doc[1] == 'отправлен':
                print(f"Документ с ID {doc_id} уже отправлен")
                return False

            # Обновляем статус документа
            cursor.execute('UPDATE documents SET status = ? WHERE id = ?', ('отправлен', doc_id))

            # Добавляем запись об отправке
            cursor.execute('''
                INSERT INTO shipments (doc_id, recipient, shipment_date, shipped_by, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (doc_id, recipient, shipment_date, user_id, notes))

            conn.commit()

            print(f"Документ с ID {doc_id} отправлен получателю '{recipient}' пользователем {user_id}")
            return True

    def return_document(self, doc_id, condition=None, notes=None, user_id=None):
        """Возврат документа"""
        return_date = datetime.now().strftime('%Y-%m-%d')

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Проверяем, существует ли документ
        cursor.execute('SELECT id, status FROM documents WHERE id = ?', (doc_id,))
        doc = cursor.fetchone()
        if not doc:
            print(f"Документ с ID {doc_id} не найден")
            conn.close()
            return False

        # Проверяем статус документа
        if doc[1] != 'отправлен':
            print(f"Документ с ID {doc_id} не был отправлен, невозможно зафиксировать возврат")
            conn.close()
            return False

        # Обновляем статус документа
        cursor.execute('UPDATE documents SET status = ? WHERE id = ?', ('возвращен', doc_id))

        # Добавляем запись о возврате
        cursor.execute('''
            INSERT INTO returns (doc_id, return_date, returned_by, condition, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (doc_id, return_date, user_id, condition, notes))

        conn.commit()
        conn.close()

        print(f"Документ с ID {doc_id} возвращен пользователем {user_id}")
        return True

    def search_documents(self, keyword):
        """Поиск документов по ключевому слову"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Используем подзапросы для получения последней отправки и возврата для каждого документа
        # А также информацию о пользователях
        cursor.execute('''
            SELECT
                d.id,
                d.doc_number,
                d.doc_title,
                d.project_number,
                d.status,
                (SELECT s.shipment_date FROM shipments s WHERE s.doc_id = d.id ORDER BY s.id DESC LIMIT 1) as shipment_date,
                (SELECT s.recipient FROM shipments s WHERE s.doc_id = d.id ORDER BY s.id DESC LIMIT 1) as recipient,
                (SELECT u.full_name FROM shipments s JOIN users u ON s.shipped_by = u.id WHERE s.doc_id = d.id ORDER BY s.id DESC LIMIT 1) as shipped_by_name,
                (SELECT r.return_date FROM returns r WHERE r.doc_id = d.id ORDER BY r.id DESC LIMIT 1) as return_date,
                (SELECT u.full_name FROM returns r JOIN users u ON r.returned_by = u.id WHERE r.doc_id = d.id ORDER BY r.id DESC LIMIT 1) as returned_by_name
            FROM documents d
            WHERE d.doc_number LIKE ? OR d.doc_title LIKE ? OR d.project_number LIKE ?
            ORDER BY d.id
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))

        docs = cursor.fetchall()
        conn.close()

        return docs


def run_cli_interface():
    """Запуск CLI-интерфейса системы учета документов"""
    system = DocTrackingSystem()
    
    # Регистрируем или авторизуем пользователя
    print("=== Авторизация ===")
    username = input("Введите ваше имя пользователя (или создайте новое): ") or "default_user"
    full_name = input("Введите ваше полное имя: ") or username
    
    # Проверяем, существует ли пользователь, если нет - создаем
    with sqlite3.connect(system.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if user:
            user_id = user[0]
            print(f"Добро пожаловать обратно, {full_name} (ID: {user_id})!")
        else:
            cursor.execute('INSERT INTO users (username, full_name) VALUES (?, ?)', (username, full_name))
            user_id = cursor.lastrowid
            conn.commit()
            print(f"Пользователь {full_name} успешно зарегистрирован с ID: {user_id}")

    while True:
        print("\n=== Система учета документов ПТО ===")
        print("1. Добавить документ")
        print("2. Отправить документ")
        print("3. Зафиксировать возврат документа")
        print("4. Просмотреть все документы")
        print("5. Найти документ")
        print("6. Выход")

        choice = input("Выберите действие (1-6): ")

        if choice == '1':
            print("\n--- Добавление документа ---")
            doc_number = input("Номер документа: ")
            doc_title = input("Наименование документа: ")
            project_number = input("Номер проекта (опционально): ") or None
            issue_date = input("Дата выпуска (ГГГГ-ММ-ДД, опционально): ") or None
            doc_type = input("Тип документа (опционально): ") or None

            system.add_document(doc_number, doc_title, project_number, issue_date, doc_type, user_id=user_id)

        elif choice == '2':
            print("\n--- Отправка документа ---")
            try:
                doc_id = int(input("ID документа для отправки: "))
                recipient = input("Получатель: ")
                shipment_date = input("Дата отправки (ГГГГ-ММ-ДД, Enter для сегодня): ") or None
                notes = input("Примечания (опционально): ") or None

                system.ship_document(doc_id, recipient, shipment_date, notes, user_id=user_id)
            except ValueError:
                print("Ошибка: ID документа должен быть числом")

        elif choice == '3':
            print("\n--- Возврат документа ---")
            try:
                doc_id = int(input("ID документа для возврата: "))
                condition = input("Состояние документа (опционально): ") or None
                notes = input("Примечания (опционально): ") or None

                system.return_document(doc_id, condition, notes, user_id=user_id)
            except ValueError:
                print("Ошибка: ID документа должен быть числом")

        elif choice == '4':
            print("\n--- Все документы ---")
            docs = system.list_documents()

            if docs:
                print(f"{'ID':<5} {'Номер':<15} {'Наименование':<30} {'Проект':<15} {'Статус':<15} {'Отправлен':<12} {'Получатель':<20} {'Отправил':<15} {'Возвращен':<12} {'Вернул':<15}")
                print("-" * 150)
                for doc in docs:
                    doc_id, doc_number, doc_title, project_number, status, shipment_date, recipient, shipped_by_name, return_date, returned_by_name = doc
                    print(f"{doc_id:<5} {doc_number:<15} {doc_title[:29]:<30} {project_number or '':<15} {status:<15} {shipment_date or '':<12} {recipient or '':<20} {shipped_by_name or '':<15} {return_date or '':<12} {returned_by_name or '':<15}")
            else:
                print("Документов нет в системе")

        elif choice == '5':
            print("\n--- Поиск документов ---")
            keyword = input("Введите ключевое слово для поиска: ")
            docs = system.search_documents(keyword)

            if docs:
                print(f"{'ID':<5} {'Номер':<15} {'Наименование':<30} {'Проект':<15} {'Статус':<15} {'Отправлен':<12} {'Получатель':<20} {'Отправил':<15} {'Возвращен':<12} {'Вернул':<15}")
                print("-" * 150)
                for doc in docs:
                    doc_id, doc_number, doc_title, project_number, status, shipment_date, recipient, shipped_by_name, return_date, returned_by_name = doc
                    print(f"{doc_id:<5} {doc_number:<15} {doc_title[:29]:<30} {project_number or '':<15} {status:<15} {shipment_date or '':<12} {recipient or '':<20} {shipped_by_name or '':<15} {return_date or '':<12} {returned_by_name or '':<15}")
            else:
                print("Документы не найдены")

        elif choice == '6':
            print("Выход из системы...")
            break
        else:
            print("Некорректный выбор. Пожалуйста, выберите число от 1 до 6.")


def main():
    """Основная функция для запуска CLI-интерфейса"""
    run_cli_interface()


if __name__ == "__main__":
    main()
