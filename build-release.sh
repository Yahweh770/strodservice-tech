#!/bin/bash

# Скрипт для автоматической сборки EXE-файла проекта в папку "release"

echo
echo "========================================"
echo "Сборка проекта Строд-Сервис Технолоджи"
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
npm install

if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось установить зависимости."
    exit 1
fi

echo
echo "2. Обновление зависимостей frontend..."
cd src/frontend
npm install

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

cd ..

echo
echo "4. Сборка Electron приложения в папку release..."

# Запускаем сборку с использованием electron-builder
npx electron-builder --config electron-builder-config.js --win

if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось собрать Electron приложение."
    exit 1
fi

# Перемещаем готовые файлы из release/dist в основную папку release
if [ -d "release/dist" ]; then
    cp -r release/dist/* release/
    rm -rf release/dist
fi

echo
echo "========================================"
echo "Сборка завершена успешно!"
echo "Результат находится в папке release"
echo "========================================"
echo