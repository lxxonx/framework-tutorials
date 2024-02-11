from fastapi import APIRouter, WebSocket


day_19_router = APIRouter(prefix="/19")


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
