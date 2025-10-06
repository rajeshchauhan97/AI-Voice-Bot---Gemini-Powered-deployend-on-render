# 🎤 Personal Voice Bot

A production-ready conversational voice bot built with **FastAPI** and **Gemini 1.5 Flash** for AI responses. Includes a modern web interface and is fully deployable on **Render**.

---

## 🌟 Features

- **AI-Powered Responses**: Uses Google Gemini 1.5 Flash for intelligent, personalized responses
- **Fallback System**: Graceful fallback to predefined responses when AI is unavailable
- **Modern Web Interface**: Responsive, mobile-friendly chat interface
- **Production Ready**: Proper error handling, logging, and health checks
- **Easy Deployment**: One-click deployment to Render.com
- **CORS Enabled**: Ready for frontend integration

---

## 📁 Project Structure

```
personal-voicebot/
├── backend/
│   ├── app.py              # FastAPI main application
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment variables
│   └── __init__.py        # Python package file
├── frontend/
│   ├── index.html         # Main HTML file
│   ├── style.css          # CSS styles
│   └── main.js            # Frontend JavaScript
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

---

## ⚡ Quick Start

### Backend Setup (Local)

1. **Clone and setup**:
```bash
git clone https://github.com/rajeshchauhan97/personal-voicebot-deployed-on-render.git
cd personal-voicebot/backend
```

2. **Create virtual environment**:
```bash
py -3.10 -m venv venv

```

3. **Activate virtual environment**:
- **Windows**: `venv\Scripts\activate`
- **Linux/macOS**: `source venv/bin/activate`

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Set environment variables**:
Create a `.env` file in `backend/`:
```
GEMINI_API_KEY=your_gemini_1.5_api_key_here
PORT=8000
```

6. **Run the backend**:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Frontend Setup (Local)

**Option 1: Using FastAPI (Recommended)**
- Backend automatically serves frontend at: [http://127.0.0.1:8000/frontend](http://127.0.0.1:8000/frontend)
- No additional setup required!

**Option 2: Using Live Server (Development)**
1. **Install live-server globally**:
```bash
npm install -g live-server
```

2. **Run frontend separately**:
```bash
cd personal-voicebot/frontend
live-server --port=3000 --entry-file=index.html
```

3. **Access frontend**: Open [http://127.0.0.1:3000](http://127.0.0.1:3000)

### Test the Application

1. **Backend API**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
2. **Web Interface**: [http://127.0.0.1:8000/frontend](http://127.0.0.1:8000/frontend)
3. **API Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

**Test Chat Endpoint**:
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"text": "Tell me your superpower"}'
```

---

## 🚀 Production Deployment

### Git Setup & Deployment

1. **Initialize Git and force push**:
```bash
cd personal-voicebot
git init
git branch -M main
git add .
git commit -m "Initial commit: Production-ready Personal Voice Bot"
git remote add origin https://github.com/rajeshchauhan97/personal-voicebot-deployed-on-render.git
git push -u origin main --force
```

2. **Deploy on Render.com**:
   - Go to [Render.com](https://render.com) → **New Web Service**
   - Connect your GitHub repository
   - Select **Branch**: `main`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT`
   - Add **Environment Variables**:
     - `GEMINI_API_KEY`: your_gemini_1.5_api_key_here
     - `PORT`: 8000

3. **Access Your Deployed App**:
   - **Web Interface**: `https://your-app-name.onrender.com/frontend`
   - **API**: `https://your-app-name.onrender.com`
   - **API Docs**: `https://your-app-name.onrender.com/docs`

---

## 📚 API Endpoints

- `GET /` - API information
- `GET /health` - Health check with AI status
- `POST /chat` - Chat endpoint (`{"text": "your question"}`)
- `GET /profile` - Suggested questions
- `GET /frontend` - Web interface (serves frontend files)
- `GET /docs` - Interactive API documentation (Swagger)

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.10+
- **AI**: Google Gemini 1.5 Flash
- **Frontend**: Vanilla JavaScript, CSS3, HTML5
- **Deployment**: Render.com
- **API Documentation**: Auto-generated Swagger/ReDoc

---

## 🔧 Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (get from [Google AI Studio](https://aistudio.google.com/))
- `PORT`: Server port (default: 8000)

### Frontend Features

- **Responsive Design**: Works on desktop and mobile
- **Real-time Chat**: Typing indicators and smooth animations
- **Quick Questions**: Pre-defined question chips for easy testing
- **Status Indicators**: Shows backend connection status
- **Error Handling**: Graceful error messages for users

### Without Gemini API Key

The bot works perfectly without an API key using intelligent fallback responses for common questions including:
- Life story and background
- Superpowers and strengths  
- Growth areas and development goals
- Work style misconceptions
- Boundary pushing approaches

---

## 💡 Usage Examples

Ask questions like:
- "What's your life story in a few sentences?"
- "What's your #1 superpower?"
- "What are your top 3 growth areas?"
- "What misconception do coworkers have about you?"
- "How do you push your boundaries and limits?"

---

## ⚠️ Important Notes

- **Gemini 1.5 Flash** is used for AI responses (free tier available)
- Without a valid API key, the app automatically uses **intelligent fallback responses**
- Frontend is served automatically via FastAPI StaticFiles at `/frontend` endpoint
- CORS is enabled for all origins (adjust for production if needed)
- The entire application (backend + frontend) deploys as one service on Render

---

## 🐛 Troubleshooting

1. **Frontend Not Loading**: Check if backend is running and accessible
2. **API Key Issues**: Verify GEMINI_API_KEY is set correctly in Render environment variables
3. **Static Files Error**: Ensure frontend folder structure is correct
4. **CORS Issues**: Frontend should be served from the same domain as backend in production
5. **Deployment Issues**: Check Render logs for detailed error messages

---

## 📫 Contact

- **GitHub**: [rajeshchauhan97](https://github.com/rajeshchauhan97)
- **Email**: sabhavathraju123@gmail.com

---

## 📄 License

MIT License - feel free to use for personal and commercial projects.

---

**🎯 Your Personal Voice Bot will be live on Render within 10 minutes of deployment! The frontend is automatically served at your-render-url/frontend**