from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from agent_controller import run_agent
import websocket_manager as ws

app = FastAPI()

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
    except:
        await ws.disconnect(websocket)


@app.get("/")
def home():
    return {"status": "AI Shopping Agent Running"}


@app.get("/search")
async def search(query: str):

    result = await run_agent(query, ws.send_update)

    return result