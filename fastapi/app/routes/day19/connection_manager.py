import json
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.rooms = {}
        self.views = 0

    async def connect(self, websocket: WebSocket, room_number: int):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.rooms.setdefault(room_number, []).append(websocket)

    def disconnect(self, websocket: WebSocket, room_number: int):
        self.rooms.get(room_number, []).remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_room(self, message: str, room_number: int, sender: str):
        for connection in self.rooms.get(room_number, []):
            await connection.send_text(json.dumps({"message": message, "user": sender}))
            self.views += 1

    async def receive_message(self, websocket: WebSocket):
        data = await websocket.receive_text()
        json_data = json.loads(data)
        message = json_data.get("message")
        return message

    def reset_views(self):
        self.views = 0
        return self.views

    def get_views(self):
        return self.views
