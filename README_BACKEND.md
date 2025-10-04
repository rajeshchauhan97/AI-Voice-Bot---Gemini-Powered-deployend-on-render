# Backend (Flask) — VoiceBot Gemini

## Quickstart (Windows, Python 3.10)
1. Create and activate virtual environment:
   ```
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # PowerShell
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set Google credentials (recommended: service account JSON):
   ```
   setx GOOGLE_APPLICATION_CREDENTIALS "C:\path\to\service-account.json"
   ```
4. Run the app (development):
   ```
   python app.py
   ```
5. Expose with ngrok for a shareable URL:
   ```
   ngrok http 8080
   ```

## Files
- app.py — main Flask app receiving audio, transcribing, generating, and returning audio response.
- gemini_client.py — wrapper around Gemini SDK calls (transcribe/generate/tts).
- requirements.txt — Python dependencies.
- Dockerfile — container image for cloud deployment.
