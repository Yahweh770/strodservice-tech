#!/bin/bash

# Скрипт для сборки .exe файла с помощью PyInstaller
# Используется в GitHub Actions для автоматического создания релизов

echo
echo "========================================"
echo "Сборка .exe файла с помощью PyInstaller"
echo "========================================"
echo

# Установка зависимостей
echo "Устанавливаем зависимости..."
pip install pyinstaller
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Создание исполняемого файла с помощью PyInstaller
echo "Создаем исполняемый файл..."
pyinstaller --onefile --windowed --add-data="pto_docs.db:." --add-data="assets/icon.ico:assets" --hidden-import=sqlite3 main.py -n doc_tracking_system

if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo "Сборка завершена успешно!"
    echo "EXE файл находится в папке dist/"
    echo "========================================"
    echo
else
    echo "Ошибка при сборке исполняемого файла"
    exit 1
fi