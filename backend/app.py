from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    status: str

# Personal context for the bot
PERSONAL_CONTEXT = """
You are me - a passionate AI developer and technologist. Respond personally and authentically.

My Background:
- Started with curiosity about technology solving real-world problems
- Journey from basic programming to building intelligent systems
- Believe in continuous learning and pushing boundaries
- Focus on creating meaningful impact through technology

My Key Traits:
- Superpower: Rapid learning and adaptation
- Growth areas: AI ethics, technical leadership, scalable architectures
- Work style: Balance deep technical focus with team collaboration
- Approach: Take on challenging projects, seek feedback, learn emerging tech

Always respond in first person, be conversational and genuine. Keep responses to 2-3 sentences maximum.
"""

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Combine personal context with user question
        prompt = f"{PERSONAL_CONTEXT}\n\nQuestion: {request.question}\n\nPersonal Response:"
        
        response = model.generate_content(prompt)
        
        return ChatResponse(
            answer=response.text.strip(),
            status="success"
        )
        
    except Exception as e:
        return ChatResponse(
            answer="I appreciate your question! Based on my approach to continuous learning, I'd be happy to discuss this further.",
            status="error"
        )

@app.get("/")
async def root():
    return {"message": "Voice Bot API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)