import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

import uuid

load_dotenv()

app = FastAPI()

sessions = {} 

def generate_session_id():
    
    return str(uuid.uuid4())

@app.post("/chat/{session_id}")
async def chat(session_id: str, message: str):
    """Handles chat messages for a specific session."""

    if session_id not in sessions:
        # Create a new session if it doesn't exist
        sessions[session_id] = {"history": [], "context": {}}

    session = sessions[session_id]
    session["history"].append({"user": message})

    # Simulate a chatbot response (replace with your actual chatbot logic)
    bot_response = f"You said: {message}.  This is a response from the chatbot in session {session_id}."
    session["history"].append({"bot": bot_response})

    return JSONResponse({"session_id": session_id, "history": session["history"]})


@app.post("/chat")
async def create_chat():
    """Creates a new chat session and returns the session ID."""
    session_id = generate_session_id()
    sessions[session_id] = {"history": [], "context": {}}
    return JSONResponse({"session_id": session_id})

@app.get("/chat/{session_id}")
async def get_chat_history(session_id: str):
    """Retrieves the chat history for a given session ID."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return JSONResponse({"session_id": session_id, "history": sessions[session_id]["history"]})

