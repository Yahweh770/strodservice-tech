#!/bin/bash

# Скрипт для автоматической сборки EXE-файла проекта в папку "release"

echo
echo "========================================"
echo "Сборка проекта StrodService"
echo "========================================"
echo

# Проверяем, установлены ли необходимые инструменты
if ! command -v npm &> /dev/null; then
    echo "ОШИБКА: npm не найден. Убедитесь, что Node.js установлен."
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "ОШИБКА: git не найден. Убедитесь, что Git установлен."
    exit 1
fi

# Создаем папку release, если она не существует
mkdir -p release

echo "1. Обновление зависимостей..."
cd "$(dirname "$0")"

# Проверяем наличие vendor-зависимостей и используем их, если доступны
if [ -d "node_modules" ]; then
    echo "Используем существующие зависимости..."
elif [ -d "vendor/node_modules" ]; then
    echo "Используем vendor-зависимости для npm..."
    ln -sf "vendor/node_modules" "node_modules"
else
    echo "Устанавливаем npm зависимости..."
    npm install
fi

if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось установить зависимости."
    exit 1
fi

echo
echo "2. Обновление зависимостей frontend..."
cd src/frontend

if [ -d "../../node_modules" ]; then
    echo "Используем существующие зависимости..."
elif [ -d "../../vendor/node_modules" ]; then
    echo "Используем vendor-зависимости для frontend..."
    if [ -d "node_modules" ]; then
        rm -rf "node_modules"
    fi
    ln -sf "../../vendor/node_modules" "node_modules"
else
    echo "Устанавливаем зависимости для frontend..."
    npm install
fi

if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось установить зависимости для frontend."
    exit 1
fi

echo
echo "3. Сборка frontend..."
npm run build

if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось собрать frontend."
    exit 1
fi

cd ../..

echo
echo "4. Установка Python зависимостей..."

# Проверяем наличие vendor-зависимостей для Python
if [ -d "vendor/python_packages" ]; then
    echo "Используем vendor-зависимости для Python..."
    pip install --find-links vendor/python_packages -r requirements.txt --no-index
else
    echo "Устанавливаем Python зависимости из интернета..."
    pip install -r requirements.txt
fi

if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось установить Python зависимости."
    exit 1
fi

echo
echo "5. Сборка Electron приложения в папку release..."

# Запускаем сборку с использованием electron-builder
npx electron-builder --config electron-builder-config.js --win

if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось собрать Electron приложение."
    exit 1
fi

# Перемещаем готовые файлы из dist в основную папку release
if [ -d "dist" ]; then
    cp -r dist/* release/
    rm -rf dist
fi

echo
echo "========================================"
echo "Сборка завершена успешно!"
echo "Результат находится в папке release"
echo "========================================"
echo