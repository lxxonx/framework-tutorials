from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.routes.day19.connection_manager import ConnectionManager


day_19_router = APIRouter(prefix="/19")

manager = ConnectionManager()


@day_19_router.websocket("/ws/ping")
async def websocket_router(websocket: WebSocket):
    await websocket.accept()
    is_active = False
    while True:
        data = await websocket.receive_text()
        if not is_active and data == "serve":
            is_active = True
            continue
        if not is_active:
            continue
        if data == "ping":
            await websocket.send_text("pong")


@day_19_router.post("/reset")
async def reset_views():
    return manager.reset_views()


@day_19_router.get("/views")
async def get_views():
    return manager.get_views()


@day_19_router.websocket("/ws/room/{room_number}/user/{user_name}")
async def room_router(websocket: WebSocket, room_number: int, user_name: str):
    await manager.connect(websocket, room_number)
    try:

        while True:
            message = await manager.receive_message(websocket)
            if len(message) > 128:
                continue
            await manager.broadcast_to_room(message, room_number, user_name)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_number)
