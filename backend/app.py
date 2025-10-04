from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import tempfile
import logging
import time
from werkzeug.utils import secure_filename
import google.generativeai as genai
import speech_recognition as sr
from pydub import AudioSegment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path to the frontend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '../frontend')

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

class PersonalVoiceBot:
    def __init__(self):
        # Using free Gemini 1.5 Flash
        self.api_key = os.environ.get('GEMINI_API_KEY', 'free_tier_default')
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Gemini configured successfully")
        except Exception as e:
            logger.error(f"Gemini configuration failed: {e}")
            self.model = None

        # Your personalized responses
        self.personal_responses = {
            "life_story": "I'm a passionate problem-solver who started my journey in technology driven by curiosity. Over the years, I've evolved from building simple applications to creating complex AI systems, always focused on making technology more accessible and solving real-world challenges through innovation.",
            "superpower": "My #1 superpower is rapid learning and adaptation. I can quickly understand complex systems and find innovative solutions by connecting different perspectives. This allows me to thrive in dynamic environments and turn challenges into opportunities.",
            "growth_areas": "I'm focused on three key growth areas: 1) Deepening expertise in AI and machine learning applications, 2) Enhancing leadership and mentorship capabilities to help teams grow, and 3) Developing strategic thinking for long-term impact in technology innovation.",
            "misconception": "People often think I'm always serious and intensely focused, but I actually thrive in collaborative, creative environments where ideas can flow freely. I believe the best solutions come from teams that balance deep work with creative exploration.",
            "boundaries": "I constantly push my boundaries by taking on projects outside my comfort zone, actively seeking diverse perspectives, and dedicating time to learn emerging technologies. I believe growth happens when we embrace challenges as opportunities."
        }

    def get_personal_response(self, question):
        """Get response in personal style"""
        question_lower = question.lower()
        
        if any(phrase in question_lower for phrase in ["life story", "about you", "tell me about yourself"]):
            return self.personal_responses["life_story"]
        elif "superpower" in question_lower or "#1" in question_lower:
            return self.personal_responses["superpower"]
        elif any(phrase in question_lower for phrase in ["grow", "growth", "areas", "improve"]):
            return self.personal_responses["growth_areas"]
        elif any(phrase in question_lower for phrase in ["misconception", "coworker", "colleague", "think about you"]):
            return self.personal_responses["misconception"]
        elif any(phrase in question_lower for phrase in ["boundaries", "limits", "comfort zone", "push"]):
            return self.personal_responses["boundaries"]
        else:
            return self._get_fallback_response(question)

    def _get_fallback_response(self, question):
        """Fallback response for unexpected questions"""
        fallback_responses = [
            "That's an interesting question. Based on my experiences, I believe in approaching challenges with curiosity and a growth mindset.",
            "I appreciate that question. From my perspective, continuous learning and adaptability are key to navigating complex situations.",
            "That's a thoughtful question. I've found that being open to new experiences and maintaining a solution-oriented approach helps in most situations."
        ]
        import random
        return random.choice(fallback_responses)

    def transcribe_audio(self, audio_path):
        """Transcribe audio to text using Google Speech Recognition"""
        wav_path = None
        try:
            recognizer = sr.Recognizer()
            
            # Convert to WAV if necessary
            if audio_path.endswith('.webm'):
                audio = AudioSegment.from_file(audio_path, format="webm")
                wav_path = audio_path + '.wav'
                audio.export(wav_path, format="wav")
                use_path = wav_path
            else:
                use_path = audio_path
            
            with sr.AudioFile(use_path) as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                logger.info(f"Transcribed: {text}")
                return text
                
        except sr.UnknownValueError:
            raise Exception("I couldn't understand the audio. Please try speaking clearly.")
        except sr.RequestError as e:
            raise Exception("Speech recognition service is currently unavailable. Please try again later.")
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            raise Exception("Error processing audio. Please try again.")
        finally:
            # Clean up converted WAV file with retry logic
            if wav_path and os.path.exists(wav_path):
                self._safe_delete_file(wav_path)

    def _safe_delete_file(self, file_path):
        """Safely delete file with retry logic for Windows"""
        for attempt in range(3):
            try:
                os.unlink(file_path)
                break
            except PermissionError:
                if attempt < 2:
                    time.sleep(0.1 * (attempt + 1))

# Initialize the bot
voice_bot = PersonalVoiceBot()

@app.route('/')
def serve_frontend():
    """Serve the main frontend page"""
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory(FRONTEND_DIR, filename)

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy", 
        "service": "Personal Voice Bot",
        "version": "1.0",
        "ready": True
    })

@app.route('/api/process', methods=['POST'])
def process_question():
    tmp_path = None
    try:
        if 'audio' in request.files:
            # Process audio file
            audio_file = request.files['audio']
            if audio_file.filename == '':
                return jsonify({"error": "No audio file selected"}), 400
            
            # Create temporary file with manual cleanup (Windows compatible)
            fd, tmp_path = tempfile.mkstemp(suffix='.webm')
            os.close(fd)  # Close the file descriptor immediately
            audio_file.save(tmp_path)
            
            # Transcribe audio
            transcript = voice_bot.transcribe_audio(tmp_path)
                
        elif request.is_json and 'text' in request.json:
            # Process text input
            transcript = request.json['text'].strip()
            if not transcript:
                return jsonify({"error": "Empty text input"}), 400
        else:
            return jsonify({"error": "No audio or text input provided"}), 400
        
        # Get personalized response
        response = voice_bot.get_personal_response(transcript)
        
        return jsonify({
            "success": True,
            "question": transcript,
            "response": response
        })
        
    except Exception as e:
        logger.error(f"Processing error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    finally:
        # Clean up temp file with retry logic
        if tmp_path and os.path.exists(tmp_path):
            voice_bot._safe_delete_file(tmp_path)

@app.route('/api/suggestions')
def get_suggestions():
    """Get suggested questions"""
    suggestions = [
        "What should we know about your life story in a few sentences?",
        "What's your #1 superpower?",
        "What are the top 3 areas you'd like to grow in?",
        "What misconception do your coworkers have about you?",
        "How do you push your boundaries and limits?",
        "What drives and motivates you?",
        "How do you handle challenges or setbacks?"
    ]
    return jsonify({"suggestions": suggestions})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)