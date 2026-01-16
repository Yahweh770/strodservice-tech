# Статус проекта "Строд-Сервис Технолоджи"

## Описание проекта

"Строд-Сервис Технолоджи" - комплексное решение для управления строительными проектами, включающее модули для ведения ГПР, учета исполнительной документации, управления материалами и отслеживания замечаний от строительного контроля. Проект включает в себя десктопное приложение на Electron с Python-бэкендом, с возможностью перехода к многопользовательскому режиму.

## Основные компоненты

### Архитектура

### Основные функциональные модули

### Технические задания

(В этом разделе будут храниться все технические задания, на основании которых осуществляется разработка)

## Недавние улучшения

### Windows-версия приложения

1. **Изменение пути к файлу лога в main.py**:
   - Было: `log_file_path = "C:/temp/strod_service_log.txt"`
   - Стало: `log_file_path = os.path.join(os.environ.get("TEMP", tempfile.gettempdir()), "strod_service_log.txt")`
   - Теперь путь к лог-файлу определяется динамически с использованием системной переменной TEMP или стандартного временного каталога Windows.

2. **Создание скрипта сборки для Windows**:
   - Создан скрипт `build-full-project.bat` с корректной логикой установки зависимостей и сборки проекта под Windows

## Структура проекта

```
.
├── src/
├── electron-app/
├── desktop-app/
├── assets/
├── main.py
├── requirements.txt
├── PROJECT_STATUS.md
└── build-full-project.bat
```

## Дополнительная информация

### Скрипт сборки для Windows (build-full-project.bat)

```batch
@echo off
setlocal enabledelayedexpansion

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Creating build directory...
if exist dist rmdir /s /q dist
mkdir dist

echo Building backend...
pyinstaller --onefile --add-data "src;src" --add-data "electron-app;electron-app" --add-data "desktop-app;desktop-app" --add-data "assets;assets" --hidden-import=fastapi.encoders --hidden-import=fastapi.openapi --hidden-import=fastapi.openapi.models --hidden-import=fastapi.openapi.utils --hidden-import=uvicorn.protocols.http.h11_impl --hidden-import=uvicorn.protocols.http.httptools_impl --hidden-import=uvicorn.protocols.websockets.websockets_impl --hidden-import=uvicorn.protocols.websockets.wsproto_impl --hidden-import=uvicorn.lifespan.on --hidden-import=uvicorn.lifespan.off --hidden-import=python-multipart --collect-all fastapi --collect-all uvicorn main.py -n strod-service-backend

echo Building desktop app...
cd desktop-app
pip install -r requirements.txt
pyinstaller --onefile --add-data "src;src" --add-data "assets;assets" --hidden-import=fastapi.encoders --hidden-import=fastapi.openapi --hidden-import=fastapi.openapi.models --hidden-import=fastapi.openapi.utils --hidden-import=uvicorn.protocols.http.h11_impl --hidden-import=uvicorn.protocols.http.httptools_impl --hidden-import=uvicorn.protocols.websockets.websockets_impl --hidden-import=uvicorn.protocols.websockets.wsproto_impl --hidden-import=uvicorn.lifespan.on --hidden-import=uvicorn.lifespan.off --hidden-import=python-multipart --collect-all fastapi --collect-all uvicorn desktop_main.py -n strod-service-desktop
cd ..

echo Building electron app frontend...
cd electron-app
npm install
npm run build
cd ..

echo Copying files to dist...
if not exist dist mkdir dist
copy /Y desktop-app\dist\strod-service-desktop.exe dist\
copy /Y dist\strod-service-backend.exe dist\
xcopy /E /I electron-app\dist electron-app\
xcopy /E /I src dist\src\
xcopy /E /I assets dist\assets\

echo Build completed successfully!
pause
```

Этот скрипт:
- Устанавливает зависимости
- Создает директорию сборки
- Собирает бэкенд с помощью PyInstaller
- Собирает десктопное приложение
- Собирает Electron-приложение
- Копирует все необходимые файлы в директорию dist