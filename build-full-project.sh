#!/bin/bash

# Скрипт для сборки полного проекта StrodService с помощью PyInstaller
# Собирает основной интерфейс, который может запускать полный функционал

echo
echo "========================================"
echo "Сборка полного проекта StrodService с помощью PyInstaller"
echo "========================================"
echo

# Установка зависимостей
echo "Устанавливаем зависимости..."
python -m pip install --upgrade pip
pip install pyinstaller

# Установка основных зависимостей проекта
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Также устанавливаем зависимости бэкенда
if [ -f "src/backend-python/requirements.txt" ]; then
    pip install -r src/backend-python/requirements.txt
fi

# Проверка наличия необходимых файлов
if [ ! -f "main.py" ]; then
    echo "Файл main.py не найден!"
    exit 1
fi

if [ ! -f "pto_docs.db" ]; then
    echo "Создаем пустую базу данных..."
    touch pto_docs.db
fi

# Создание исполняемого файла с помощью PyInstaller
echo "Создаем исполняемый файл для полного проекта..."
pyinstaller --onefile --console \
    --add-data="pto_docs.db:." \
    --add-data="assets/icon.ico:assets" \
    --add-data="config.py:." \
    --add-data="src:src" \
    --hidden-import=sqlite3 \
    --hidden-import=sqlalchemy \
    --hidden-import=fastapi \
    --hidden-import=uvicorn \
    --hidden-import=uvicorn.protocols \
    --hidden-import=uvicorn.protocols.http \
    --hidden-import=uvicorn.protocols.websockets \
    --hidden-import=jinja2 \
    --clean \
    main.py -n StrodService-Full

if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo "Сборка полного проекта завершена успешно!"
    echo "EXE файл находится в папке dist/"
    echo "Запустите его с командой: ./StrodService-Full full-project"
    echo "========================================"
    echo
    ls -la dist/
else
    echo "Ошибка при сборке исполняемого файла"
    exit 1
fi