#!/bin/bash

# Run script for Hugging Face Model Security Scanner

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run build.sh first:"
    echo "  ./build.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if required environment variables are set
if [ -z "$MODEL_SECURITY_CLIENT_ID" ] || [ -z "$MODEL_SECURITY_CLIENT_SECRET" ] || [ -z "$TSG_ID" ]; then
    echo "Warning: Required environment variables not set."
    echo "Please set the following environment variables:"
    echo "  export MODEL_SECURITY_CLIENT_ID='your_client_id'"
    echo "  export MODEL_SECURITY_CLIENT_SECRET='your_client_secret'"
    echo "  export TSG_ID='your_tsg_id'"
    echo ""
    echo "Or create a .env file with these variables."
fi

# Run the web application
echo "Starting Hugging Face Model Security Scanner..."
echo "Open your browser and navigate to http://localhost:5000"
python web_app.py