# app/main.py
from fastapi import FastAPI, WebSocket
from app.websocket_handler import WebSocketHandler

app = FastAPI()
handler = WebSocketHandler()

@app.websocket("/transcribe")
async def websocket_endpoint(websocket: WebSocket):
    await handler.handle_connection(websocket)

def run():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)