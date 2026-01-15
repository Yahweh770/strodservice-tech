# План улучшения приложения "Строд-Сервис Технолоджи" для командного использования

## Текущее состояние

Приложение "Строд-Сервис Технолоджи" представляет собой десктопное приложение на Electron с Python-бэкендом (FastAPI) и React-фронтендом. В настоящее время приложение спроектировано для использования одним пользователем на одном компьютере.

## Проблемы текущей архитектуры для командного использования

1. **Однопользовательская архитектура**: Приложение запускается как десктопное приложение на отдельном компьютере, что ограничивает доступ к данным только одному пользователю.
2. **Локальная база данных**: Используется SQLite база данных, которая не поддерживает эффективно многопользовательский доступ.
3. **Отсутствие централизованного сервера**: Нет общего сервера, где могут храниться и синхронизироваться данные для всей команды.
4. **Ограниченная масштабируемость**: Архитектура не позволяет легко добавлять новых пользователей или распределять нагрузку.

## План улучшений

### Этап 1: Модернизация архитектуры

#### 1.1. Разделение приложения на независимые компоненты
- **Backend-сервер**: Самостоятельный FastAPI сервер, который может работать на отдельном сервере
- **Frontend-приложение**: Веб-интерфейс, который может подключаться к backend-серверу
- **Electron-обертка**: Необязательная десктопная обертка для локального использования

#### 1.2. Изменение способа запуска
- Добавить возможность запуска backend-сервера независимо от Electron-приложения
- Реализовать конфигурацию подключения frontend к удаленному или локальному серверу

#### 1.3. Обновление файла конфигурации
```bash
# В package.json добавить новые скрипты:
"start:server": "cd src/backend-python && uvicorn main:app --host 0.0.0.0 --port 8000 --reload",
"start:web": "cd src/frontend && npm start",
"start:standalone": "concurrently \"npm run start:server\" \"npm run start:web\"",
```

### Этап 2: Улучшение системы аутентификации и авторизации

#### 2.1. Расширение модели пользователя
- Добавить поля для информации о компании, подразделении и должности
- Реализовать иерархию ролей (администратор, менеджер проектов, инженер ПТО, прораб и т.д.)
- Добавить поддержку групп пользователей

#### 2.2. Реализация системы разграничения доступа
- Контроль доступа на уровне объектов (например, доступ к определенным проектам)
- Ролевая модель с настраиваемыми правами
- Журнал аудита действий пользователей

### Этап 3: Переход на PostgreSQL

#### 3.1. Обновление конфигурации базы данных
- Заменить SQLite на PostgreSQL в production-окружении
- Реализовать систему миграций для безопасного перехода
- Обеспечить совместимость с существующими данными

#### 3.2. Обновление моделей данных
- Адаптировать все модели под возможности PostgreSQL
- Добавить поддержку конкурентного доступа
- Оптимизировать запросы для многопользовательской среды

### Этап 4: Реализация многопользовательской синхронизации

#### 4.1. Добавление WebSocket-соединений
- Реализовать реал-тайм уведомления об изменениях
- Синхронизация изменений между всеми активными пользователями
- Система блокировок для предотвращения конфликта редактирования

#### 4.2. Оптимизация производительности
- Кэширование часто запрашиваемых данных
- Пагинация больших наборов данных
- Асинхронная обработка тяжелых операций

### Этап 5: Развертывание и масштабирование

#### 5.1. Подготовка к production-развертыванию
- Настройка Docker-контейнеров для каждого компонента
- Реализация CI/CD пайплайна
- Настройка мониторинга и логирования

#### 5.2. Поддержка облачных платформ
- Подготовка приложения для развертывания на AWS, Azure или Google Cloud
- Настройка автоматического масштабирования
- Обеспечение отказоустойчивости

## Технические детали реализации

### Изменения в main.py (Backend)
```python
# Добавить поддержку конфигурации базы данных через переменные окружения
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./strod_service_tech.db")

if "postgresql" in DATABASE_URL.lower():
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,
        max_overflow=0,
        pool_pre_ping=True,
    )
else:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### Изменения в системе аутентификации
```python
# В auth.py добавить поддержку refresh токенов и продления сессий
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### Добавление WebSocket для синхронизации
```python
# В main.py добавить WebSocket маршруты
from fastapi import WebSocket, WebSocketDisconnect
from collections import defaultdict

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.user_connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[websocket.client.host] = websocket
        self.user_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int):
        self.active_connections.pop(websocket.client.host, None)
        if user_id in self.user_connections:
            self.user_connections[user_id].remove(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_user(self, user_id: int, message: str):
        connections = self.user_connections.get(user_id, [])
        for connection in connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Обработка входящих сообщений
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
```

## Потенциальные риски и решения

1. **Переход с SQLite на PostgreSQL**
   - Риск: Потеря данных при миграции
   - Решение: Тщательное тестирование миграций, создание резервных копий

2. **Проблемы с производительностью при увеличении числа пользователей**
   - Риск: Замедление работы приложения
   - Решение: Оптимизация запросов, внедрение кэширования, использование CDN

3. **Проблемы с безопасностью в многопользовательской среде**
   - Риск: Несанкционированный доступ к данным
   - Решение: Тщательная проверка прав доступа, шифрование чувствительных данных

## Заключение

Переход на многопользовательскую архитектуру значительно повысит эффективность работы команды и позволит использовать приложение в распределенной среде. Важно поэтапно внедрять изменения, тщательно тестировать каждый этап и обеспечивать обратную совместимость с существующими данными.