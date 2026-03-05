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

# Copy application code
COPY . .

# Make scripts executable
RUN chmod +x model_scan.sh build.sh

# Create a wrapper script for installing model-security-client at runtime
RUN echo '#!/bin/bash\n\
if [ -n "$MODEL_SECURITY_CLIENT_ID" ] && [ -n "$MODEL_SECURITY_CLIENT_SECRET" ] && [ -n "$TSG_ID" ]; then\n\
    echo "Installing model-security-client..."\n\
    PYPI_URL=$(/app/model_scan.sh)\n\
    if [ $? -eq 0 ]; then\n\
        pip install "model-security-client[all]" --extra-index-url "$PYPI_URL"\n\
        echo "model-security-client installed successfully"\n\
    else\n\
        echo "Failed to install model-security-client"\n\
    fi\n\
else\n\
    echo "MODEL_SECURITY_CLIENT_ID, MODEL_SECURITY_CLIENT_SECRET, and TSG_ID not set. Skipping model-security-client installation."\n\
fi\n\
\n\
# Start the web application\n\
exec python web_app.py' > /app/start.sh && chmod +x /app/start.sh

# Install Python dependencies (excluding model-security-client which will be installed at runtime)
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Launch the web server with runtime installation of model-security-client
CMD ["/app/start.sh"]
