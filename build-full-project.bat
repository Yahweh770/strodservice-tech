@echo off
setlocal enabledelayedexpansion

echo ========================================
echo StrodService Full Project Build Process
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if npm is available
npm --version >nul 2>&1
if errorlevel 1 (
    echo Error: npm is not installed or not in PATH
    pause
    exit /b 1
)

echo Installing Python dependencies...
pip install --upgrade pip
if errorlevel 1 (
    echo Error: Failed to upgrade pip
    pause
    exit /b 1
)

pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install Python requirements
    pause
    exit /b 1
)

echo.
echo Installing Node.js dependencies for desktop app...
cd desktop-app
if exist node_modules (
    echo Removing existing node_modules...
    rmdir /s /q node_modules
)
npm install --no-audit --no-fund
if errorlevel 1 (
    echo Error: Failed to install desktop app dependencies
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo Installing Node.js dependencies for electron app...
cd electron-app
if exist node_modules (
    echo Removing existing node_modules...
    rmdir /s /q node_modules
)
npm install --no-audit --no-fund
if errorlevel 1 (
    echo Error: Failed to install electron app dependencies
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo Creating build directory...
if exist dist rmdir /s /q dist
mkdir dist
if errorlevel 1 (
    echo Error: Failed to create dist directory
    pause
    exit /b 1
)

echo.
echo Building backend service executable...
pip install pyinstaller
if errorlevel 1 (
    echo Error: Failed to install PyInstaller
    pause
    exit /b 1
)

REM Build the main backend executable with corrected paths
pyinstaller --clean --onefile ^
    --add-data "src;src" ^
    --add-data "assets;assets" ^
    --add-data "config.py;." ^
    --hidden-import=fastapi.encoders ^
    --hidden-import=fastapi.openapi ^
    --hidden-import=fastapi.openapi.models ^
    --hidden-import=fastapi.openapi.utils ^
    --hidden-import=uvicorn.protocols.http.h11_impl ^
    --hidden-import=uvicorn.protocols.http.httptools_impl ^
    --hidden-import=uvicorn.protocols.websockets.websockets_impl ^
    --hidden-import=uvicorn.protocols.websockets.wsproto_impl ^
    --hidden-import=uvicorn.lifespan.on ^
    --hidden-import=uvicorn.lifespan.off ^
    --hidden-import=python-multipart ^
    --collect-all fastapi ^
    --collect-all uvicorn ^
    --collect-all sqlalchemy ^
    --collect-all pydantic ^
    --collect-all jwt ^
    --collect-all passlib ^
    --collect-all bcrypt ^
    --name strod-service-backend ^
    main.py

if errorlevel 1 (
    echo Error: Failed to build backend executable
    pause
    exit /b 1
)

echo.
echo Packaging desktop application...
cd desktop-app
npx electron-builder --win --x64 --config electron-builder-config.js
if errorlevel 1 (
    echo Warning: Desktop app packaging failed, continuing with other builds
)
cd ..

echo.
echo Copying built files to distribution folder...

REM Create necessary directories
mkdir dist 2>nul
mkdir dist\backend 2>nul
mkdir dist\desktop-app 2>nul
mkdir dist\electron-app 2>nul
mkdir dist\docs 2>nul
mkdir dist\assets 2>nul

REM Copy backend executable
if exist dist\strod-service-backend.exe (
    copy /Y dist\strod-service-backend.exe dist\ 1>nul
)

REM Copy source code and assets
xcopy /E /I /Q src dist\src\ 1>nul
xcopy /E /I /Q assets dist\assets\ 1>nul
copy /Y config.py dist\ 1>nul 2>nul

REM Copy documentation
copy /Y README.md dist\ 1>nul
copy /Y LICENSE dist\ 1>nul
copy /Y requirements.txt dist\ 1>nul

REM Copy database file if exists
if exist pto_docs.db copy /Y pto_docs.db dist\ 1>nul

REM Copy desktop app build if exists
if exist desktop-app\dist (
    xcopy /E /I /Q desktop-app\dist\*.* dist\desktop-app\ 1>nul
)

REM Copy electron app build if exists
if exist electron-app\dist (
    xcopy /E /I /Q electron-app\dist\*.* dist\electron-app\ 1>nul
)

REM Create startup scripts
(
echo @echo off
echo.
echo echo Starting StrodService Backend Server...
echo echo ========================================
echo.
echo REM Check if backend executable exists
echo if not exist strod-service-backend.exe (
echo     echo Error: Backend executable not found
echo     pause
echo     exit /b 1
echo )
echo.
echo echo Launching backend server on http://localhost:8000
echo echo Press Ctrl+C to stop the server
echo.
echo start /B strod-service-backend.exe full-project ^> server.log 2^>^&1
echo.
echo echo Opening web interface in browser...
echo timeout /t 3 /nobreak
echo start http://localhost:8000
echo.
echo echo Server logs are available in server.log
echo echo Press any key to stop the server
echo pause
echo taskkill /f /im strod-service-backend.exe 2^>nul
echo del server.log 2^>nul
) > dist\start-server.bat

(
echo @echo off
echo.
echo echo StrodService Release Package
echo echo =============================
echo.
echo echo Files included:
echo dir /b /ad 2^>nul
echo dir /b *.exe *.py *.db *.md *.txt *.json *.js 2^>nul
echo.
echo echo To start the server: run start-server.bat
echo echo To view documentation: open README.md
echo.
echo pause
) > dist\info.bat

echo.
echo ========================================
echo Build completed successfully!
echo Distribution package created in: dist\
echo ========================================
echo.
echo Contents of dist directory:
dir /s dist
echo.
echo To start the application, go to the dist directory and run start-server.bat
echo.
pause