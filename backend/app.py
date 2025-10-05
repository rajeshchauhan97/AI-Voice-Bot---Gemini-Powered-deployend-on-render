from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os
import uvicorn
import requests
import asyncio

# Load .env file
load_dotenv()

# Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# Canned responses
CANNED_RESPONSES = {
    "life story": "I was trained on a broad range of text to help people learn, build, and write. I focus on clarity, friendly explanations, and practical next steps.",
    "superpower": "My #1 superpower is turning complex ideas into clear, actionable explanations and examples — I make things easier to understand and use.",
    "growth areas": "Top three areas I'd like to grow in: 1) maintaining longer-term context across multi-step projects, 2) staying current with the latest research and events, and 3) producing even more concise, actionable plans.",
    "coworker misconception": "A common misconception is that I always give final answers — I'm most useful when we iterate together, ask follow-ups, and test ideas.",
    "push boundaries": "I push boundaries by trying new formats, running small experiments, asking better questions, and learning quickly from feedback and failures.",
}

# Detect intent
def detect_intent(text: str):
    t = text.lower()
    if any(k in t for k in ["life story", "about your life", "who are you", "tell me about your life"]):
        return "life story"
    if any(k in t for k in ["superpower", "#1 superpower", "top superpower"]):
        return "superpower"
    if any(k in t for k in ["grow in", "growth areas", "areas you'd like to grow", "top 3 areas", "top 3"]):
        return "growth areas"
    if any(k in t for k in ["misconception", "coworker", "coworkers think", "misunderstand"]):
        return "coworker misconception"
    if any(k in t for k in ["push your boundaries", "push your limits", "push boundaries", "how do you push"]):
        return "push boundaries"
    return None

# Gemini chat call
def call_gemini_chat(prompt: str):
    if not GEMINI_API_KEY:
        return None
    url = "https://generativeai.googleapis.com/v1beta2/models/text-bison-001:generate"
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": {"text": prompt},
        "temperature": 0.6,
        "maxOutputTokens": 300
    }
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=15)
        if resp.status_code != 200:
            return None
        res = resp.json()
        return res.get("candidates", [{}])[0].get("content", "").strip()
    except Exception:
        return None

# Root route
@app.get("/", response_class=HTMLResponse)
async def root():
    if os.path.exists("frontend/index.html"):
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h2>Welcome to Personal Voice Bot API!</h2><p>Use the /chat endpoint to interact.</p>"

# Chat endpoint
@app.post("/chat")
async def chat(req: Request):
    payload = await req.json()
    text = payload.get("text", "").strip()
    if not text:
        return {"ok": False, "error": "No text provided"}

    intent = detect_intent(text)

    # Try Gemini if available
    if GEMINI_API_KEY:
        loop = asyncio.get_event_loop()
        ai_answer = await loop.run_in_executor(None, lambda: call_gemini_chat(text))
        if ai_answer:
            return {"ok": True, "source": "gemini", "text": ai_answer}

    # Use canned responses
    if intent and intent in CANNED_RESPONSES:
        return {"ok": True, "source": "canned", "text": CANNED_RESPONSES[intent]}

    # Fallback
    generic = ("I don't have an AI key set on the server, so here's a helpful assistant-style reply: "
               "Please try rephrasing or ask a specific follow-up.")
    return {"ok": True, "source": "fallback", "text": generic}

# Audio transcription (still OpenAI Whisper if you want)
@app.post("/transcribe-audio")
async def transcribe_audio(file: UploadFile = File(...)):
    if not GEMINI_API_KEY:
        return {"ok": False, "error": "Server has no GEMINI_API_KEY for transcription."}
    return {"ok": False, "error": "Audio transcription is not implemented for Gemini yet."}

# Run app
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
