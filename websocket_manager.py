from fastapi import WebSocket

connections = []

async def connect(ws: WebSocket):
    await ws.accept()
    connections.append(ws)

async def disconnect(ws: WebSocket):
    connections.remove(ws)

async def send_update(message: str):
    for ws in connections:
        try:
            await ws.send_text(message)
        except:
            pass