FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .
COPY frontend/ ../frontend/

# Create non-root user
RUN useradd -m -u 1000 voicebot
USER voicebot

# Expose port
EXPOSE $PORT

# Start command for production
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]