from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from Chatbot import startSession2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def firstTest():
    print('hello')
    return {'msg':'hello'}

@app.post("/chat")
async def sendMessage(request: Request):
    data = await request.json()
    message = data.get("message")
    return StreamingResponse(startSession2(message), media_type="text/plain")