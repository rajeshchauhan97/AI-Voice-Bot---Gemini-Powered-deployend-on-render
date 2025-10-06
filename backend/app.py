# backend/app.py

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
import os
import uvicorn
import base64
import tempfile
import speech_recognition as sr
import logging
import datetime

# --- Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("personal_voice_bot")

# --- App Initialization ---
app = FastAPI(title="Personal Voice Bot", version="1.0.0")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Serve Frontend ---
frontend_path = "../frontend"
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# --- Personal Responses ---
PERSONAL_RESPONSES = {
    "life_story": "I'm a passionate technology professional who started with computer science and evolved into AI development. I focus on creating solutions that simplify complex technology.",
    "superpower": "My #1 superpower is rapid learning and clear communication, helping me explain complex concepts simply and bridge gaps between technical teams and users.",
    "growth_areas": "I aim to grow in: 1) AI ethics, 2) Leadership and mentorship, 3) Product strategy and user-centered design.",
    "misconception": "People think I'm purely technical, but I'm very people-oriented. Collaboration and understanding different perspectives drive the best solutions.",
    "boundaries": "I push my boundaries by taking on new projects, seeking diverse feedback, and dedicating time to learn new skills each week."
}

# --- Helper Functions ---
def get_personal_response(question: str) -> str:
    q = question.lower().strip()
    if any(kw in q for kw in ["life story", "about you", "background", "tell me about yourself"]):
        return PERSONAL_RESPONSES["life_story"]
    if any(kw in q for kw in ["superpower", "super power", "strength", "#1"]):
        return PERSONAL_RESPONSES["superpower"]
    if any(kw in q for kw in ["grow", "improve", "development", "areas", "top 3"]):
        return PERSONAL_RESPONSES["growth_areas"]
    if any(kw in q for kw in ["misconception", "people think", "coworker", "coworkers"]):
        return PERSONAL_RESPONSES["misconception"]
    if any(kw in q for kw in ["boundaries", "limits", "push", "challenge"]):
        return PERSONAL_RESPONSES["boundaries"]
    return "That's an interesting question! Feel free to ask about my background, strengths, or approach to challenges."

def transcribe_audio(audio_bytes: bytes) -> str:
    """Convert audio bytes to text using speech recognition"""
    try:
        recognizer = sr.Recognizer()
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(audio_bytes)
            temp_file.flush()
            with sr.AudioFile(temp_file.name) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)
            os.unlink(temp_file.name)
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio. Please speak clearly."
    except Exception:
        return "Error processing audio. Please try again."

# --- Uptime ---
START_TIME = datetime.datetime.utcnow()

# --- Routes ---
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return "<h2>Frontend not found. Place your frontend files in ../frontend/</h2>"

@app.get("/api/health")
async def health_check():
    uptime = datetime.datetime.utcnow() - START_TIME
    return {
        "status": "healthy",
        "message": "Personal Voice Bot API is running",
        "version": "1.0.0",
        "uptime_seconds": int(uptime.total_seconds())
    }

@app.get("/api/sample-questions")
async def sample_questions():
    return {
        "questions": [
            "What should we know about your life story in a few sentences?",
            "What's your #1 superpower?",
            "What are the top 3 areas you'd like to grow in?",
            "What misconception do your coworkers have about you?",
            "How do you push your boundaries and limits?"
        ]
    }

@app.post("/api/chat")
async def chat(request: Request):
    try:
        payload = await request.json()
        msg_type = payload.get("type", "text")

        if msg_type == "text":
            question = payload.get("message", "").strip()
            if not question:
                raise HTTPException(status_code=400, detail="No message provided")
            response = get_personal_response(question)
            return {"response": response, "type": "text"}

        elif msg_type == "audio":
            audio_data = payload.get("audio", "")
            if not audio_data:
                raise HTTPException(status_code=400, detail="No audio data provided")
            try:
                audio_bytes = base64.b64decode(audio_data.split(",")[1] if "," in audio_data else audio_data)
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid audio data")
            question = transcribe_audio(audio_bytes)
            response = get_personal_response(question) if "Sorry" not in question and "Error" not in question else question
            return {"response": response, "transcribed_question": question, "type": "audio"}

        else:
            raise HTTPException(status_code=400, detail="Invalid message type")

    except Exception as e:
        logger.error(f"Error in /api/chat: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# --- Run App ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
