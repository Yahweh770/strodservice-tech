#!/bin/bash

# Скрипт для сборки .exe файла с помощью PyInstaller
# Используется в GitHub Actions для автоматического создания релизов

echo
echo "========================================"
echo "Сборка .exe файла StrodService с помощью PyInstaller"
echo "========================================"
echo

# Установка зависимостей
echo "Устанавливаем зависимости..."
python -m pip install --upgrade pip
pip install pyinstaller
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
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
echo "Создаем исполняемый файл..."
pyinstaller --onefile --console \
    --add-data="pto_docs.db:." \
    --add-data="assets/icon.ico:assets" \
    --add-data="config.py:." \
    --hidden-import=sqlite3 \
    --hidden-import=sqlalchemy \
    --clean \
    main.py -n StrodService

if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo "Сборка завершена успешно!"
    echo "EXE файл находится в папке dist/"
    echo "========================================"
    echo
    ls -la dist/
else
    echo "Ошибка при сборке исполняемого файла"
    exit 1
fi