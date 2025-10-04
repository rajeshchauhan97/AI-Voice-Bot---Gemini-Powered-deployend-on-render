import google.generativeai as genai
import os
import logging

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY', 'free_tier_default')
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Gemini client initialized successfully")
        except Exception as e:
            logger.error(f"Gemini client initialization failed: {e}")
            self.model = None

    def generate_text(self, prompt, model="gemini-1.5-flash"):
        """Generate text using Gemini"""
        if not self.model:
            return "Service temporarily unavailable."
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Text generation error: {e}")
            return "I encountered an error while generating a response."

    def transcribe_audio(self, audio_path, model="gemini-1.5-flash"):
        """Placeholder for audio transcription - using speech_recognition instead"""
        # This method is kept for compatibility
        # Actual transcription happens in app.py using speech_recognition
        return "Audio transcription placeholder"