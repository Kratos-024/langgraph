from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List
from Chatbot import startStream, getSessions, getChats

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def home():
    return {'msg': 'API is running'}

@app.get('/getChatSessions')
def fetch_all_sessions():
    try:
        sessions = getSessions()  
        return {
            'sessions': sessions,
            'statusCode': 200
        }
    except Exception as e:
        print(f"Error fetching sessions: {e}")
        return {'sessions': [], 'statusCode': 500}

@app.get("/getChats") 
def fetch_chat_history(currentSessionId: str):
    try:
        chats = getChats(currentSessionId.strip())
        return {
            'history': chats,  
            'statusCode': 200
        }
    except Exception as e:
        print(f"Error fetching chats: {e}")
        return {'history': [], 'statusCode': 500, 'error': str(e)}

@app.post("/chat")
async def sendMessage(request: Request):
    try:
        data = await request.json()
        message = data.get("message")
        session_id = data.get("sessionId") 
        
        return StreamingResponse(
            startStream(message, session_id), 
            media_type="text/plain"
        )
    except Exception as e:
        print(f"Streaming error: {e}")
        return {"error": "Failed to start stream"}