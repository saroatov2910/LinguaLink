from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from translation import translate_text
from connection_manager import ConnectionManager
from config import language_codes

# Create the main FastAPI application instance
app = FastAPI()

# Initialize the connection manager for handling WebSocket clients
manager = ConnectionManager()

# Add CORS middleware to allow cross-origin requests from any source
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,  # Allow credentials (cookies, auth headers)
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# WebSocket endpoint for chat translation
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    preferred_lang = await websocket.receive_json()
    await manager.connect(websocket, preferred_lang["lang"])
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data["message"], websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
