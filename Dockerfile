# Use official Python base image
FROM python:3.11-slim

# Install system dependencies for Tesseract, Poppler, and others
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirement and install
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app/ .

# Expose the API port
EXPOSE 5000

# Run the app
CMD ["python", "main.py"]
