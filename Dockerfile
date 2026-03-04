# Use Python 3.12 as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make the script executable
RUN chmod +x model_scan.sh

# Expose port 5000
EXPOSE 5000

# Copy the env file
COPY .env .env

# Load environment variables from .env and run model_scan.sh with secrets
RUN export $(cat .env | xargs) && \
    ./model_scan.sh | xargs -I {} pip install "model-security-client[all]" --extra-index-url {}

# Launch the web server
CMD ["python", "web_app.py"]
