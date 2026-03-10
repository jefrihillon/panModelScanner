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

# Install model-security-client directly
RUN pip install model-security-client

# Copy application code
COPY . .

# Make the script executable
RUN chmod +x model_scan.sh

# Expose port 5000
EXPOSE 5000

# Launch the web server (runtime environment variables will be provided via docker run or docker-compose)
CMD ["python", "web_app.py"]