from pathlib import Path

from fastapi import FastAPI, Query, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from agent_controller import run_agent
import websocket_manager as ws

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
INDEX_PATH = BASE_DIR / "static" / "index.html"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except Exception:
        await ws.disconnect(websocket)


@app.get("/")
def home():
    if INDEX_PATH.exists():
        return FileResponse(INDEX_PATH)
    return {"status": "AI Shopping Agent Running", "ui": "index file missing"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
async def search(query: str = Query(..., min_length=2)):
    result = await run_agent(query, ws.send_update)

    return result