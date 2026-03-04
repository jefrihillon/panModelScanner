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

ENV MODEL_SECURITY_CLIENT_ID=""
ENV MODEL_SECURITY_CLIENT_SECRET=""
ENV TSG_ID=""
ENV MODEL_SECURITY_API_ENDPOINT="https://api.sase.paloaltonetworks.com/aims"

# Grab an auth token via the ./model_scan.sh script and install the model-security-client package
RUN ./model_scan.sh | xargs -I {} pip install "model-security-client[all]" --extra-index-url {}

# Launch the web server
CMD ["python", "web_app.py"]