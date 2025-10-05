# Personal Voice Bot — Production-ready ZIP

This project provides a universally user-friendly voice bot web app (frontend + backend) that answers questions in the assistant's voice. It supports:
- Browser-based voice recording (Web Speech API)
- Text input fallback
- Browser TTS (speechSynthesis)
- Server-side AI (OpenAI) if `OPENAI_API_KEY` is set on the host; otherwise deterministic canned replies are used.
- Docker and Render deployment instructions.

## Structure
personal-voicebot/
├─ backend/
│  ├─ app.py
│  ├─ requirements.txt
│  ├─ Dockerfile
│  └─ Procfile
├─ frontend/
│  ├─ index.html
│  ├─ app.js
│  └─ package.json
├─ docker-compose.yml
└─ README.md

## Quick local testing (recommended)
### Option A — Run with Docker Compose (recommended)
1. Install Docker and Docker Compose.
2. In the project root:
   ```bash
   docker-compose up --build
   ```
3. Open the frontend: http://localhost:3000
   Backend: http://localhost:8000

### Option B — Run backend locally (Python)
1. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```
3. Serve frontend by opening `frontend/index.html` in a browser (or use live-server / simple static server).

## Deploy to Render (recommended)
### Backend
1. Create a new **Web Service** on Render, connecting your GitHub repo and selecting the `backend` folder.
2. Build Command:
   ```
   pip install -r requirements.txt
   ```
3. Start Command:
   ```
   uvicorn app:app --host 0.0.0.0 --port $PORT
   ```
4. In Render dashboard -> Environment, add `OPENAI_API_KEY` as a secret if you want live AI responses.

### Frontend
1. Create a new **Static Site** on Render, connecting the same repo and selecting the `frontend` folder.
2. Build Command:
   ```
   npm install && npm run build
   ```
   (This project uses a small static page; you can also host the static files by serving them from the backend.)
3. In the frontend, point the backend base URL to the backend service URL (or use the same origin if backend serves frontend).

## Notes
- **No end-user API key entry is required.** Add `OPENAI_API_KEY` only on the server (Render/Heroku environment variables).
- For production, restrict CORS to your frontend origin rather than '*'.
- Consider adding rate-limiting and authentication if you expose the app publicly.

## Sample questions the bot answers (canned)
- "What should we know about your life story in a few sentences?"
- "What's your #1 superpower?"
- "What are the top 3 areas you'd like to grow in?"
- "What misconception do your coworkers have about you?"
- "How do you push your boundaries and limits?"

