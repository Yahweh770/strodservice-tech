@echo off
chcp 65001
title Build Script

echo ========================================
echo Сборка проекта СТРОД-СЕРВИС ТЕХНОЛОДЖИ
echo ========================================
echo.

REM Проверяем Git
git --version >nul 2>&1 || (
    echo ОШИБКА: Git не найден. Убедитесь, что Git установлен.
    pause
    exit /b 1
)

REM Проверяем Node.js
node --version >nul 2>&1 || (
    echo ОШИБКА: Node.js не найден. Убедитесь, что Node.js установлен.
    pause
    exit /b 1
)

REM Проверяем Python
python --version >nul 2>&1 || (
    echo ОШИБКА: Python не найден. Убедитесь, что Python установлен.
    pause
    exit /b 1
)

echo Установка зависимостей...
cd /d "%~dp0"

REM Устанавливаем npm зависимости
call npm install --no-audit --no-fund

REM Устанавливаем Python зависимости
pip install -r requirements.txt

REM Устанавливаем vendor зависимости
call npm run install-vendor

echo Сборка Electron-приложения...
cd electron-app
call npm install --no-audit --no-fund
call npm run build

echo Сборка Desktop-приложения...
cd ../desktop-app
call npm install --no-audit --no-fund
call npm run build

echo Сборка Frontend...
cd ../src/frontend
call npm install --no-audit --no-fund
call npm run build

echo.
echo === Сборка завершена ===
pause