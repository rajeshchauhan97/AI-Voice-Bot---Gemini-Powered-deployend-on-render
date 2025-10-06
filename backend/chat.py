import os
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_gemini_response(user_input: str) -> str:
    if not GEMINI_API_KEY:
        return "Fallback response: Please set GEMINI_API_KEY"
    url = "https://api.gemini.ai/v1/chat"
    payload = {
        "model": "gemini-1.5-flash",
        "messages": [{"role": "user", "content": user_input}]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_API_KEY}"
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=15)
        r.raise_for_status()
        data = r.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
    except Exception as e:
        print("Gemini API error:", e)
        return "Error in AI response"
