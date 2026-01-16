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

# Создаем временный каталог для сборки
mkdir -p build_temp

# Копируем все необходимые файлы и директории
cp -r src/ build_temp/src/ 2>/dev/null || echo "Директория src не найдена или пустая"
cp -r electron-app/ build_temp/electron-app/ 2>/dev/null || echo "Директория electron-app не найдена или пустая"
cp -r desktop-app/ build_temp/desktop-app/ 2>/dev/null || echo "Директория desktop-app не найдена или пустая"
cp -r assets/ build_temp/assets/ 2>/dev/null || echo "Директория assets не найдена или пустая"
cp main.py config.py requirements.txt pto_docs.db build_temp/ 2>/dev/null || touch build_temp/pto_docs.db

# Переходим во временный каталог
cd build_temp

# Создание исполняемого файла с помощью PyInstaller
pyinstaller --onefile --console \
    --add-data="pto_docs.db:." \
    --add-data="assets:assets" \
    --add-data="config.py:." \
    --add-data="src:src" \
    --add-data="electron-app:electron-app" \
    --add-data="desktop-app:desktop-app" \
    --hidden-import=sqlite3 \
    --hidden-import=sqlalchemy \
    --hidden-import=fastapi \
    --hidden-import=uvicorn \
    --hidden-import=uvicorn.protocols \
    --hidden-import=uvicorn.protocols.http \
    --hidden-import=uvicorn.protocols.websockets \
    --hidden-import=jinja2 \
    --hidden-import=cryptography \
    --hidden-import=passlib \
    --hidden-import=pydantic \
    --hidden-import=websockets \
    --hidden-import=python-multipart \
    --hidden-import=alembic \
    --clean \
    main.py -n StrodService-Complete

BUILD_STATUS=$?

# Возвращаемся в исходную директорию
cd ..

# Копируем результат в основную директорию, если сборка успешна
if [ $BUILD_STATUS -eq 0 ]; then
    if [ -f "build_temp/dist/StrodService-Complete" ] || [ -f "build_temp/dist/StrodService-Complete.exe" ]; then
        cp "build_temp/dist/StrodService-Complete"* . 2>/dev/null || cp "build_temp/dist/StrodService-Complete.exe" . 2>/dev/null
        echo
        echo "========================================"
        echo "Сборка полного проекта завершена успешно!"
        echo "EXE файл находится в текущей папке"
        echo "========================================"
        echo
    fi
fi

# Удаляем временный каталог
rm -rf build_temp

if [ $BUILD_STATUS -ne 0 ]; then
    echo "Ошибка при сборке исполняемого файла"
    exit 1
fi