# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy backend folder contents
COPY backend/ ./backend/

# Set working dir to backend
WORKDIR /app/backend

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Start the backend
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
