# Строд-Сервис Технолоджи - Desktop Application

## Описание

Проект представляет собой десктопное приложение на базе Electron, которое объединяет фронтенд (React) и бэкенд (Python/FastAPI) в единое целое.

## Архитектура

- **Frontend**: React-приложение в папке `src/frontend`
- **Backend**: Python/FastAPI сервер в папке `src/backend-python`
- **Electron**: Главный процесс в файле `electron-main.js`, preload-скрипт в `preload.js`

## Особенности реализации

1. **Интеграция**: Electron автоматически запускает Python-бэкенд при старте приложения
2. **Коммуникация**: Frontend взаимодействует с бэкендом через IPC-каналы Electron
3. **Сборка**: Приложение может быть собрано в исполняемый файл для различных платформ

## Запуск приложения

### Разработка

1. Установите зависимости:
```bash
npm install
cd src/frontend && npm install
cd ../backend-python && pip install -r requirements.txt
```

2. Запустите приложение:
```bash
# Способ 1: Запуск Electron с автоматическим запуском бэкенда
npm run start-electron

# Способ 2: Параллельный запуск всех компонентов
npm run start:backend  # в одном терминале
npm run start:frontend # во втором терминале
npm run start-electron # в третьем терминале
```

### Сборка

1. Соберите фронтенд:
```bash
npm run build-frontend
```

2. Соберите Electron-приложение:
```bash
npm run dist-electron  # для создания установщика
```

## API взаимодействие

Frontend может обращаться к Python-бэкенду следующим образом:

```javascript
// В любом React-компоненте
const data = await window.electronAPI.sendRequest('GET', '/some-endpoint', null);
const result = await window.electronAPI.sendRequest('POST', '/another-endpoint', { key: 'value' });
```

## Файлы проекта

- `electron-main.js` - главный процесс Electron, запускает Python-бэкенд
- `preload.js` - скрипт для безопасного взаимодействия между процессами
- `package.json` - зависимости и скрипты проекта
- `electron-builder-config.js` - конфигурация для сборки установщика