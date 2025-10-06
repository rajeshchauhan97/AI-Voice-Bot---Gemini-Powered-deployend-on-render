from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from chat import get_gemini_response
from fastapi.staticfiles import StaticFiles
import os
import uvicorn

app = FastAPI(title="Personal Voice Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = os.path.join(os.path.dirname(__file__), '../frontend')
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("text")
    if not user_input:
        return {"response": "Please provide a message."}
    response = get_gemini_response(user_input)
    return {"response": response}

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
