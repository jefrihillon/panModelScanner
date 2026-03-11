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

# Make the script executable
RUN chmod +x model_scan.sh

# Use BuildKit secrets to mount environment variables during build
# and run model_scan.sh with secrets (no credentials stored in image)
RUN --mount=type=secret,id=id,target=./id.txt \
    --mount=type=secret,id=secret,target=./secret.txt \
    --mount=type=secret,id=tsg,target=./tsg.txt \
    export MODEL_SECURITY_CLIENT_ID=$(cat /run/secrets/id) && \
    export MODEL_SECURITY_CLIENT_SECRET=$(cat /run/secrets/secret) && \
    export TSG_ID=$(cat /run/secrets/tsg) && \
    ./model_scan.sh | xargs -I {} pip install "model-security-client[all]" --extra-index-url {}

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 5000
EXPOSE 5000

# Launch the web server (runtime environment variables will be provided via docker run or docker-compose)
CMD ["python", "main.py"]
