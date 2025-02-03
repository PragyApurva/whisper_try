# app/websocket_handler.py
from fastapi import WebSocket, WebSocketDisconnect
import json
from app.audio_processor import AudioProcessor
from app.response_generator import ResponseGenerator

class WebSocketHandler:
    def __init__(self):
        self.audio_processor = AudioProcessor()
        self.response_generator = ResponseGenerator()

    async def handle_connection(self, websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                try:
                    data = await websocket.receive_text()
                    audio_data = json.loads(data)
                    transcription = self.audio_processor.transcribe(audio_data)
                    if transcription:
                        response = self.response_generator.generate_response(transcription)
                        await websocket.send_text(json.dumps({"response": response}))
                    else:
                        await websocket.send_text(json.dumps({"response": "No speech detected"}))
                except json.JSONDecodeError:
                    await websocket.send_text(json.dumps({"error": "Invalid JSON data"}))
                except Exception as e:
                    await websocket.send_text(json.dumps({"error": str(e)}))
        except WebSocketDisconnect:
            print("Client disconnected")