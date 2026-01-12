# Строд-Сервис Технолоджи

## Описание проекта

Этот проект представляет собой комплексное решение для управления строительством от компании "Строд-Сервис Технолоджи". В состав проекта входят:

- Backend на Python (FastAPI)
- Frontend на React
- Desktop-приложение на Electron
- Документация

## Структура проекта

- `src/` - исходный код
  - `backend-python/` - Python-бэкенд на FastAPI
  - `frontend/` - React-фронтенд
  - `docs/` - документация
  - `shared/` - общие файлы
- `electron-main.js` - главный файл Electron-приложения
- `preload.js` - preload-скрипт для Electron
- `electron-builder-config.js` - конфигурация сборки Electron-приложения
- `example-api-usage.js` - пример использования API
- `README_ELECTRON.md` - документация по Electron-приложению
- `main.py` - основной Python-файл
- `requirements.txt` - зависимости Python
- `package.json` - зависимости и скрипты Node.js

## Запуск проекта

Для подробного описания запуска и разработки см. `README_ELECTRON.md`

## Сборка релиза

Для быстрой сборки готового EXE-файла в папку `release` используйте один из следующих скриптов:

- `build-release.bat` — для Windows (двойной клик или запуск из командной строки)
- `build-release.sh` — для Linux/macOS (выполнить `./build-release.sh`)

Скрипты автоматически:
1. Устанавливают все зависимости
2. Собирают React-фронтенд
3. Создают EXE-файл приложения с помощью Electron Builder
4. Помещают результат в папку `release`
