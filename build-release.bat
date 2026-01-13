@echo off
chcp 65001
title Build Script

echo ========================================
echo Building Project STROD-SERVICE TECHNOLOGY
echo ========================================
echo.

REM Check Git
git --version >nul 2>&1 || (
    echo ERROR: Git not found. Make sure Git is installed.
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1 || (
    echo ERROR: Node.js not found. Make sure Node.js is installed.
    pause
    exit /b 1
)

REM Check Python
python --version >nul 2>&1 || (
    echo ERROR: Python not found. Make sure Python is installed.
    pause
    exit /b 1
)

echo Installing dependencies...
cd /d "%~dp0"

REM Install npm dependencies
call npm install --no-audit --no-fund

REM Install Python dependencies
if exist requirements.txt (
    pip install -r requirements.txt
)

REM Install vendor dependencies
call npm run install-vendor

echo Building Electron application...
if exist electron-app (
    cd electron-app
    call npm install --no-audit --no-fund
    call npm run build
    cd ..
)

echo Building Desktop application...
if exist desktop-app (
    cd desktop-app
    call npm install --no-audit --no-fund
    call npm run build
    cd ..
)

echo Building Frontend...
if exist src/frontend (
    cd src/frontend
    call npm install --no-audit --no-fund
    call npm run build
    cd ../..
)

echo.
echo === Build completed ===
pause