@echo off
chcp 65001
title Build Script - StrodService

echo ========================================
echo Building Document Tracking System EXE
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1 || (
    echo ERROR: Python not found. Make sure Python is installed.
    pause
    exit /b 1
)

echo Installing dependencies...
cd /d "%~dp0"

REM Install Python dependencies
python -m pip install --upgrade pip
pip install pyinstaller
if exist requirements.txt (
    echo Installing Python dependencies...
    pip install -r requirements.txt
)

REM Check if main.py exists
if not exist "main.py" (
    echo File main.py not found!
    pause
    exit /b 1
)

REM Create empty database if it doesn't exist
if not exist "pto_docs.db" (
    echo Creating empty database...
    type nul > pto_docs.db
)

REM Build executable with PyInstaller
echo Building executable with PyInstaller...
pyinstaller --onefile --console --add-data="pto_docs.db;." --add-data="assets/icon.ico;assets" --add-data="config.py;." --hidden-import=sqlite3 --hidden-import=sqlalchemy --clean main.py -n StrodService

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Build completed successfully!
    echo Executable file is located in dist/ folder
    echo ========================================
    echo.
    
    REM Copy database and assets to dist folder if they don't exist
    if not exist dist mkdir dist
    if exist pto_docs.db (
        copy /Y pto_docs.db dist\
    )
    if not exist dist\assets (
        mkdir dist\assets
    )
    if exist assets\icon.ico (
        copy /Y assets\icon.ico dist\assets\
    )
    if exist config.py (
        copy /Y config.py dist\
    )
    
    echo Files in dist folder:
    dir /B dist\
) else (
    echo Error during build process!
    exit /b 1
)

pause