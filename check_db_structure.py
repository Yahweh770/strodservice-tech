#!/usr/bin/env python3
"""
Скрипт для проверки структуры базы данных системы учета документов ПТО
"""

import sqlite3

def check_db_structure():
    print("=== Проверка структуры базы данных ===\n")
    
    # Подключаемся к базе данных
    conn = sqlite3.connect('pto_docs.db')
    cursor = conn.cursor()
    
    # Получаем список таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Существующие таблицы:")
    for table in tables:
        print(f"  - {table[0]}")
    print()
    
    # Проверяем структуру таблицы documents
    print("Структура таблицы 'documents':")
    cursor.execute("PRAGMA table_info(documents);")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]} ({col[2]}) - {'NOT NULL' if col[3] == 1 else 'NULL'}, default: {col[4]}")
    print()
    
    # Проверяем структуру таблицы shipments
    print("Структура таблицы 'shipments':")
    cursor.execute("PRAGMA table_info(shipments);")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]} ({col[2]}) - {'NOT NULL' if col[3] == 1 else 'NULL'}, default: {col[4]}")
    print()
    
    # Проверяем структуру таблицы returns
    print("Структура таблицы 'returns':")
    cursor.execute("PRAGMA table_info(returns);")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]} ({col[2]}) - {'NOT NULL' if col[3] == 1 else 'NULL'}, default: {col[4]}")
    print()
    
    # Проверяем содержимое таблиц
    print("Содержимое таблиц:")
    
    # Считаем количество записей в каждой таблице
    cursor.execute("SELECT COUNT(*) FROM documents;")
    doc_count = cursor.fetchone()[0]
    print(f"  Таблица 'documents': {doc_count} записей")
    
    cursor.execute("SELECT COUNT(*) FROM shipments;")
    ship_count = cursor.fetchone()[0]
    print(f"  Таблица 'shipments': {ship_count} записей")
    
    cursor.execute("SELECT COUNT(*) FROM returns;")
    ret_count = cursor.fetchone()[0]
    print(f"  Таблица 'returns': {ret_count} записей")
    
    conn.close()

if __name__ == "__main__":
    check_db_structure()