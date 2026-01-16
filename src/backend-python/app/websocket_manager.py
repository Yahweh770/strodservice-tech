from fastapi import WebSocket, WebSocketDisconnect
from collections import defaultdict
import json
from typing import Dict, List


class ConnectionManager:
    """Класс для управления WebSocket соединениями"""
    
    def __init__(self):
        # Активные соединения: websocket -> user_id
        self.active_connections: Dict[WebSocket, int] = {}
        # Список соединений для каждого пользователя
        self.user_connections: Dict[int, List[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, user_id: int):
        """Подключить WebSocket соединение для пользователя"""
        await websocket.accept()
        self.active_connections[websocket] = user_id
        self.user_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Отключить WebSocket соединение"""
        if websocket in self.active_connections:
            user_id = self.active_connections[websocket]
            self.active_connections.pop(websocket)
            if user_id in self.user_connections:
                try:
                    self.user_connections[user_id].remove(websocket)
                    if not self.user_connections[user_id]:
                        del self.user_connections[user_id]
                except ValueError:
                    pass  # Соединение уже удалено

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Отправить личное сообщение через WebSocket"""
        await websocket.send_text(message)

    async def broadcast_to_user(self, user_id: int, message: str):
        """Отправить сообщение всем соединениям конкретного пользователя"""
        connections = self.user_connections.get(user_id, [])
        for connection in connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                # Если соединение разорвано, удаляем его
                self.disconnect(connection)

    async def broadcast_to_all(self, message: str):
        """Отправить сообщение всем активным соединениям"""
        for connection in list(self.active_connections.keys()):
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                # Если соединение разорвано, удаляем его
                self.disconnect(connection)

    def get_user_connections_count(self, user_id: int) -> int:
        """Получить количество активных соединений для пользователя"""
        return len(self.user_connections.get(user_id, []))


# Глобальный экземпляр менеджера соединений
manager = ConnectionManager()