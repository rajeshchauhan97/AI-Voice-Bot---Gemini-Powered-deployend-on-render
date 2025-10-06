import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Personal Voice Bot API",
    description="AI-powered voice bot",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    response: str
    status: str

# Personal responses data
PERSONAL_RESPONSES = {
    "life_story": "I'm a passionate technologist who started coding at a young age and evolved into building AI systems. My journey spans from simple websites to complex machine learning solutions, always driven by curiosity and making a positive impact through technology.",
    "superpower": "My #1 superpower is rapid learning and adaptation. I can quickly understand complex systems and find innovative solutions, which allows me to thrive in fast-paced environments.",
    "growth_areas": "1) Deepening expertise in AI ethics, 2) Enhancing technical leadership, 3) Mastering scalable system architecture",
    "misconception": "Many coworkers think I'm always serious, but I actually enjoy humor and building strong team connections.",
    "boundaries": "I constantly push my boundaries by taking on challenging projects and learning emerging technologies."
}

def get_response(question: str) -> str:
    """Get appropriate response based on question content"""
    question_lower = question.lower()
    
    if any(phrase in question_lower for phrase in ['life story', 'about you', 'background']):
        return PERSONAL_RESPONSES['life_story']
    elif any(phrase in question_lower for phrase in ['superpower', 'strength', 'best at']):
        return PERSONAL_RESPONSES['superpower']
    elif any(phrase in question_lower for phrase in ['grow', 'improve', 'development areas']):
        return PERSONAL_RESPONSES['growth_areas']
    elif any(phrase in question_lower for phrase in ['misconception', 'coworker', 'colleague']):
        return PERSONAL_RESPONSES['misconception']
    elif any(phrase in question_lower for phrase in ['boundaries', 'limits', 'challenge']):
        return PERSONAL_RESPONSES['boundaries']
    else:
        return "I appreciate your question! Based on my approach to continuous learning, I believe this is an area worth exploring."

@app.get("/")
async def read_root():
    return {"message": "Personal Voice Bot API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Voice Bot API"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        question = request.text.strip()
        
        if not question:
            raise HTTPException(status_code=400, detail="Question text is required")
        
        logger.info(f"Received question: {question}")
        response = get_response(question)
        
        return ChatResponse(response=response, status="success")
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/profile")
async def get_profile():
    return {
        "suggested_questions": [
            "What should we know about your life story?",
            "What's your #1 superpower?",
            "What are your top 3 growth areas?",
            "What misconception do coworkers have about you?",
            "How do you push your boundaries?"
        ]
    }

# Serve frontend files
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/frontend")
async def serve_frontend():
    return FileResponse('../frontend/index.html')