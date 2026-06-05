FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Tesseract + OpenCV
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-hin \
    tesseract-ocr-kan \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project into the container
COPY . .

# Create writable upload/extracted folders
RUN mkdir -p static/uploads extracted

# Expose Hugging Face Spaces port
EXPOSE 7860

# Start the Flask app
CMD ["python", "app.py"]
