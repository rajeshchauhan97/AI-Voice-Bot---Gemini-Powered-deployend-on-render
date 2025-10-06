from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Personal Voice Bot API",
    description="Voice bot that responds with personal answers",
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

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    status: str

@app.get("/")
async def root():
    return {"message": "Personal Voice Bot API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Voice Bot API"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        question = request.question.lower().strip()
        
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        logger.info(f"Processing question: {question}")
        
        # Personal responses as YOU would respond
        if any(phrase in question for phrase in ['life story', 'about you', 'background', 'tell me about yourself']):
            answer = "I'm a passionate technologist who started coding at a young age and evolved into building AI systems. My journey spans from simple websites to complex machine learning solutions, always driven by curiosity and making a positive impact through technology. I believe in continuous learning and pushing boundaries to create meaningful solutions."
        
        elif any(phrase in question for phrase in ['superpower', 'strength', 'best at', 'what are you good at']):
            answer = "My #1 superpower is rapid learning and adaptation. I can quickly understand complex systems and find innovative solutions, which allows me to thrive in fast-paced environments and constantly evolve with emerging technologies. This enables me to tackle new challenges effectively and deliver results efficiently."
        
        elif any(phrase in question for phrase in ['grow', 'improve', 'development areas', 'weakness', 'growth areas']):
            answer = "My top 3 areas for growth are: 1) Deepening expertise in AI ethics and responsible development practices, 2) Enhancing technical leadership and mentorship capabilities to help others grow, and 3) Mastering scalable system architecture and cloud-native technologies for building robust applications."
        
        elif any(phrase in question for phrase in ['misconception', 'coworker', 'colleague', 'think about you', 'wrong about']):
            answer = "Many coworkers think I'm always serious and completely focused on work, but I actually enjoy humor and building strong team connections. I balance deep technical work with creating a positive, collaborative environment where everyone can thrive and contribute their best work."
        
        elif any(phrase in question for phrase in ['boundaries', 'limits', 'challenge', 'comfort zone', 'push yourself']):
            answer = "I constantly push my boundaries by taking on challenging projects outside my comfort zone, learning emerging technologies before they become mainstream, and actively seeking constructive feedback to identify and address my blind spots. I believe growth happens when we step outside what's familiar."
        
        else:
            answer = "That's an interesting question! Based on my approach to continuous learning and growth, I believe this is an area worth exploring. Could you provide a bit more context about what you'd like to know?"
        
        return ChatResponse(answer=answer, status="success")
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Serve frontend files
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/frontend")
async def serve_frontend():
    return FileResponse('../frontend/index.html')

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)