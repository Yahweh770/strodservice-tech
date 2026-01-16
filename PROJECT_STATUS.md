# Статус проекта "Строд-Сервис Технолоджи"

## Описание проекта

"Строд-Сервис Технолоджи" - комплексное решение для управления строительными проектами, включающее модули для ведения ГПР, учета исполнительной документации, управления материалами и отслеживания замечаний от строительного контроля. Проект включает в себя десктопное приложение на Electron с Python-бэкендом, с возможностью перехода к многопользовательскому режиму.

## Основные компоненты

### Архитектура

Проект состоит из следующих основных компонентов:
- Python-бэкенд на FastAPI
- Web-фронтенд на React (TypeScript)
- Electron-приложение для десктопной версии
- Система управления базами данных SQLAlchemy

### Основные функциональные модули

1. Модуль ведения ГПР (График производства работ)
2. Модуль учета исполнительной документации
3. Модуль управления материалами
4. Модуль отслеживания замечаний от строительного контроля

### UX/UI дизайн

Проект включает современный UX/UI дизайн, реализованный в виде React-приложения в директории `/src/frontend`. Дизайн включает:
- Адаптивный интерфейс для работы на различных устройствах
- Интуитивно понятные формы и элементы управления
- Современные компоненты и стили
- Поддержку темной и светлой тем
- Интерактивные элементы для лучшего пользовательского опыта

### Технические задания

(В этом разделе будут храниться все технические задания, на основании которых осуществляется разработка)

## Недавние улучшения

### Windows-версия приложения

1. **Изменение пути к файлу лога в main.py**:
   - Было: `log_file_path = "C:/temp/strod_service_log.txt"`
   - Стало: `log_file_path = os.path.join(os.environ.get("TEMP", tempfile.gettempdir()), "strod_service_log.txt")`
   - Теперь путь к лог-файлу определяется динамически с использованием системной переменной TEMP или стандартного временного каталога Windows.

2. **Исправление скрипта сборки для Windows**:
   - Исправлен скрипт `build-full-project.bat` - устранена ошибка, связанная с попыткой установки Python-зависимостей для Electron-приложения (desktop-app)
   - Заменена команда `pip install -r requirements.txt` на `npm install` в директории desktop-app
   - Заменена попытка сборки desktop-приложения через PyInstaller на корректную сборку через electron-builder
   - Обновлено копирование файлов из результата сборки Electron-приложения

3. **Создание файла конфигурации для electron-builder**:
   - Создан файл `desktop-app/electron-builder-config.js` для явной конфигурации процесса сборки Electron-приложения

## Структура проекта

```
.
├── src/
│   ├── backend-python/
│   ├── docs/
│   ├── frontend/          # React-приложение с UX/UI дизайном
│   └── shared/
├── electron-app/
├── desktop-app/           # Electron-приложение
│   ├── electron-builder-config.js    # Файл конфигурации для сборки
│   ├── package.json
│   ├── main.js
│   ├── index.html
│   ├── styles.css
│   └── preload.js
├── assets/
├── main.py               # Основной Python-бэкенд
├── requirements.txt      # Python-зависимости
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
npm install
npx electron-builder --win --config electron-builder-config.js
cd ..

echo Building electron app frontend...
cd electron-app
npm install
npm run build
cd ..

echo Copying files to dist...
if not exist dist mkdir dist
xcopy /E /I desktop-app\dist\*.* dist\desktop-app\
copy /Y dist\strod-service-backend.exe dist\
xcopy /E /I electron-app\dist dist\electron-app\
xcopy /E /I src dist\src\
xcopy /E /I assets dist\assets\

echo Build completed successfully!
pause
```

Этот скрипт:
- Устанавливает зависимости
- Создает директорию сборки
- Собирает бэкенд с помощью PyInstaller
- Собирает десктопное приложение с помощью electron-builder (исправлено)
- Собирает Electron-приложение
- Копирует все необходимые файлы в директорию dist