
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from translation import translate_text
from connection_manager import ConnectionManager

app = FastAPI()
    
manager = ConnectionManager()

