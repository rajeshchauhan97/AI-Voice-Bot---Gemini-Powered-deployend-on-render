from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import uvicorn
import requests
import asyncio

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

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

# Canned responses for example questions
CANNED_RESPONSES = {
    "life story": "I was trained on a broad range of text to help people learn, build, and write. I focus on clarity, friendly explanations, and practical next steps.",
    "superpower": "My #1 superpower is turning complex ideas into clear, actionable explanations and examples — I make things easier to understand and use.",
    "growth areas": "Top three areas I'd like to grow in: 1) maintaining longer-term context across multi-step projects, 2) staying current with the latest research and events, and 3) producing even more concise, actionable plans.",
    "coworker misconception": "A common misconception is that I always give final answers — I'm most useful when we iterate together, ask follow-ups, and test ideas.",
    "push boundaries": "I push boundaries by trying new formats, running small experiments, asking better questions, and learning quickly from feedback and failures.",
}

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

def call_openai_chat(prompt: str):
    if not OPENAI_API_KEY:
        return None
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful, concise, and friendly assistant. Answer in the voice of the assistant."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 300,
        "temperature": 0.6,
    }
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=15)
        if resp.status_code != 200:
            return None
        res = resp.json()
        return res.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    except Exception:
        return None

# Root route (fixes 404)
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

    # Try OpenAI if available
    if OPENAI_API_KEY:
        loop = asyncio.get_event_loop()
        ai_answer = await loop.run_in_executor(None, lambda: call_openai_chat(text))
        if ai_answer:
            return {"ok": True, "source": "openai", "text": ai_answer}

    # Use canned responses
    if intent and intent in CANNED_RESPONSES:
        return {"ok": True, "source": "canned", "text": CANNED_RESPONSES[intent]}

    generic = ("I don't have an AI key set on the server, so here's a helpful assistant-style reply: "
               "Please try rephrasing or ask a specific follow-up.")
    return {"ok": True, "source": "fallback", "text": generic}

# Audio transcription
@app.post("/transcribe-audio")
async def transcribe_audio(file: UploadFile = File(...)):
    if not OPENAI_API_KEY:
        return {"ok": False, "error": "Server has no OPENAI_API_KEY for transcription."}
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    files = {"file": (file.filename, await file.read())}
    data = {"model": "whisper-1"}
    try:
        resp = requests.post(url, headers=headers, files=files, data=data, timeout=60)
        if resp.status_code != 200:
            return {"ok": False, "error": resp.text}
        return resp.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}

# Run app
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
