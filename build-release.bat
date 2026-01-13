@echo off
REM Скрипт для автоматической сборки EXE-файла проекта в папку "release"

echo.
echo ========================================
echo Сборка проекта Строд-Сервис Технолоджи
echo ========================================
echo.

REM Проверяем, установлены ли необходимые инструменты
where npm >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ОШИБКА: npm не найден. Убедитесь, что Node.js установлен.
    pause
    exit /b 1
)

where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ОШИБКА: git не найден. Убедитесь, что Git установлен.
    pause
    exit /b 1
)

REM Создаем папку release, если она не существует
if not exist "release" mkdir "release"

echo 1. Обновление зависимостей...
cd /d "%~dp0"

REM Проверяем наличие vendor-зависимостей и используем их, если доступны
if exist "node_modules" (
    echo Используем существующие зависимости...
) else (
    if exist "vendor\node_modules" (
        echo Используем vendor-зависимости для npm...
        mklink /D "node_modules" "vendor\node_modules"
    ) else (
        echo Устанавливаем npm зависимости...
        npm install
    )
)

if %ERRORLEVEL% neq 0 (
    echo ОШИБКА: Не удалось установить зависимости.
    pause
    exit /b 1
)

echo.
echo 2. Обновление зависимостей frontend...
cd src/frontend

if exist "..\..\node_modules" (
    echo Используем существующие зависимости...
) else (
    if exist "..\..\vendor\node_modules" (
        echo Используем vendor-зависимости для frontend...
        if exist "node_modules" rmdir /S /Q "node_modules"
        mklink /D "node_modules" "..\..\vendor\node_modules"
    ) else (
        echo Устанавливаем зависимости для frontend...
        npm install
    )
)

if %ERRORLEVEL% neq 0 (
    echo ОШИБКА: Не удалось установить зависимости для frontend.
    cd ../..
    pause
    exit /b 1
)

echo.
echo 3. Сборка frontend...
npm run build

if %ERRORLEVEL% neq 0 (
    echo ОШИБКА: Не удалось собрать frontend.
    cd ../..
    pause
    exit /b 1
)

cd ../..

echo.
echo 4. Установка Python зависимостей...

REM Проверяем наличие vendor-зависимостей для Python
if exist "vendor\python_packages" (
    echo Используем vendor-зависимости для Python...
    pip install --find-links vendor\python_packages -r requirements.txt --no-index
) else (
    echo Устанавливаем Python зависимости из интернета...
    pip install -r requirements.txt
)

if %ERRORLEVEL% neq 0 (
    echo ОШИБКА: Не удалось установить Python зависимости.
    pause
    exit /b 1
)

echo.
echo 5. Сборка Electron приложения в папку release...

REM Запускаем сборку с использованием electron-builder
npx electron-builder --config electron-builder-config.js --win

if %ERRORLEVEL% neq 0 (
    echo ОШИБКА: Не удалось собрать Electron приложение.
    pause
    exit /b 1
)

REM Перемещаем готовые файлы из dist в основную папку release
if exist "dist" (
    xcopy /E /I /Y "dist" "release"
    rmdir /S /Q "dist"
)

echo.
echo ========================================
echo Сборка завершена успешно!
echo Результат находится в папке release
echo ========================================
echo.

pause