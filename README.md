# 🎤 Personal Voice Bot

A conversational voice bot built with **FastAPI** and **Gemini 1.5** for AI responses. Includes a frontend for chat and optional audio transcription. Fully deployable on **Render**.

---

## 🌟 Features

- AI-powered chat using **Gemini 1.5** (`text-bison-001`) model.
- Fallback canned responses when AI key is missing.
- Serve frontend (`HTML/JS`) from FastAPI.
- CORS enabled for frontend integration.
- Optional audio transcription placeholder (OpenAI Whisper can be used).
- Ready for Docker deployment and Render cloud deployment.

---

## 📁 Project Structure

```

personal-voicebot/
├─ backend/
│  ├─ app.py
│  ├─ requirements.txt
│  ├─ .env
│  └─ venv/            # Local virtual environment
├─ frontend/
│  ├─ index.html
│  ├─ style.css
│  └─ main.js
├─ Dockerfile
└─ README.md

<<<<<<< HEAD
````

---

=======
# 🎤 Personal Voice Bot

A conversational voice bot built with **FastAPI** and **Gemini 1.5** for AI responses. Includes a frontend for chat and optional audio transcription. Fully deployable on **Render**.

---

## 🌟 Features

- AI-powered chat using **Gemini 1.5** (`text-bison-001`) model.
- Fallback canned responses when AI key is missing.
- Serve frontend (`HTML/JS`) from FastAPI.
- CORS enabled for frontend integration.
- Optional audio transcription placeholder (OpenAI Whisper can be used).
- Ready for Docker deployment and Render cloud deployment.


>>>>>>> 46c2feafb12cfe72ce9c777df563aadccb51dd76
## ⚡ Prerequisites

- Python 3.10+
- Node.js 18+ (optional for frontend development)
- Git
- Render account
- Gemini API key (`GEMINI_API_KEY`)

---

## 🐍 Backend Setup (Local)

1. **Clone the repo**:
   ```bash
   git clone https://github.com/rajeshchauhan97/personal-voicebot-deployed-on-render.git
   cd personal-voicebot/backend
````

2. **Create virtual environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:

   * Windows:

     ```bash
     venv\Scripts\activate
     ```
   * Linux/macOS:

     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:

   ```bash
<<<<<<< HEAD
pip install -r requirements.txt
   ```

5. **Set environment variables**:

   * Create a `.env` file in `backend/`:

     ```
     GEMINI_API_KEY=your_gemini_1.5_api_key_here
     PORT=8000
     ```

6. **Run the backend**:

   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

7. **Test locally**:

   * Open [http://127.0.0.1:8000](http://127.0.0.1:8000)
   * Chat endpoint: POST `/chat` with JSON:

     ```json
     { "text": "Tell me your superpower" }
     ```

---

## 💻 Frontend Setup (Optional)

1. **Install live-server globally (Node.js required)**:

   ```bash
   npm install -g live-server
   ```

=======
   pip install -r requirements.txt
   ```

5. **Set environment variables**:

   * Create a `.env` file in `backend/`:

     ```
     GEMINI_API_KEY=your_gemini_1.5_api_key_here
     PORT=8000
     ```

6. **Run the backend**:

   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

7. **Test locally**:

   * Open [http://127.0.0.1:8000](http://127.0.0.1:8000)
   * Chat endpoint: POST `/chat` with JSON:

     ```json
     { "text": "Tell me your superpower" }
     ```

---

## 💻 Frontend Setup (Optional)

1. **Install live-server globally (Node.js required)**:

   ```bash
   npm install -g live-server
   ```

>>>>>>> 46c2feafb12cfe72ce9c777df563aadccb51dd76
2. **Run frontend**:

   ```bash
   cd ../frontend
   live-server --port=3000 --entry-file=index.html
   ```

3. Open [http://127.0.0.1:3000](http://127.0.0.1:3000) in your browser.

---

## 🐙 Git Setup for Deployment

1. **Initialize Git** (if not already):

   ```bash
   git init
   git branch -M main
   ```

2. **Add remote**:

   ```bash
   git remote add origin https://github.com/rajeshchauhan97/personal-voicebot-deployed-on-render.git
   ```

3. **Commit changes**:

   ```bash
   git add .
   git commit -m "Initial commit: Personal Voice Bot with Gemini"
   ```

4. **Pull remote first** (if repo is not empty):

   ```bash
   git pull origin main --allow-unrelated-histories
   ```

5. **Push to GitHub**:

   ```bash
   git push -u origin main
   ```

---

## 🚀 Deploy to Render

1. Go to [Render.com](https://render.com) → **New Web Service**.
2. Connect GitHub repository.
3. Select **Branch:** `main`.
4. **Build Command**:

   ```bash
   pip install -r backend/requirements.txt
   ```
5. **Start Command**:

   ```bash
   uvicorn app:app --host 0.0.0.0 --port $PORT
   ```
6. Add **Environment Variables** in Render:

   ```
   GEMINI_API_KEY = your_gemini_1.5_api_key_here
   PORT = 8000
   ```
7. Deploy! Your backend will be live on Render URL. The frontend is served automatically via FastAPI StaticFiles.

---
<<<<<<< HEAD

## ⚠️ Notes

* Gemini 1.5 is required for AI responses. Without a valid key, the app will return **fallback canned responses**.
* Audio transcription for Gemini is **not implemented** yet.
* For production, update CORS `allow_origins` to your frontend domain.

---

## 📫 Contact

* GitHub: [rajeshchauhan97](https://github.com/rajeshchauhan97)
* Email: `sabhavathraju123@gmail.com`

---

=======

## ⚠️ Notes
>>>>>>> 46c2feafb12cfe72ce9c777df563aadccb51dd76

* Gemini 1.5 is required for AI responses. Without a valid key, the app will return **fallback canned responses**.
* Audio transcription for Gemini is **not implemented** yet.
* For production, update CORS `allow_origins` to your frontend domain.

---

## 📫 Contact

* GitHub: [rajeshchauhan97](https://github.com/rajeshchauhan97)
* Email: `sabhavathraju123@gmail.com`

---
