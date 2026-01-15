@echo off
chcp 65001
title Build Script - Document Tracking System

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
if exist requirements.txt (
    echo Installing Python dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
)

REM Install PyInstaller if not already installed
pip install pyinstaller

echo Building executable with PyInstaller...
REM Create the executable from the main document tracking system
pyinstaller --onefile --console --add-data "pto_docs.db;." --add-data "assets/icon.ico;assets" --hidden-import=sqlite3 --clean doc_tracking_system.py -n doc_tracking_system.exe

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
    
    echo Files in dist folder:
    dir /B dist\
) else (
    echo Error during build process!
    exit /b 1
)

pause