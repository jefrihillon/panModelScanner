#!/bin/bash

# Build script for Hugging Face Model Security Scanner

# Exit on any error
set -e

echo "Building Hugging Face Model Security Scanner..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Check if required environment variables are set
if [ -z "$MODEL_SECURITY_CLIENT_ID" ] || [ -z "$MODEL_SECURITY_CLIENT_SECRET" ] || [ -z "$TSG_ID" ]; then
    echo "Warning: Required environment variables not set."
    echo "Please set the following environment variables:"
    echo "  export MODEL_SECURITY_CLIENT_ID='your_client_id'"
    echo "  export MODEL_SECURITY_CLIENT_SECRET='your_client_secret'"
    echo "  export TSG_ID='your_tsg_id'"
    echo ""
    echo "Or create and source an .env file with these variables and run the build script again."
fi

# Install model-security-client
echo "Installing model-security-client..."
chmod +x model_scan.sh
./model_scan.sh | xargs -I {} pip install "model-security-client[all]" --extra-index-url {}

# Install dependencies
echo "Installing remainingdependencies..."
pip install -r requirements.txt

echo "Build complete!"
echo ""
echo "To run the web application:"
echo "  source venv/bin/activate"
echo "  export MODEL_SECURITY_CLIENT_ID='your_client_id'"
echo "  export MODEL_SECURITY_CLIENT_SECRET='your_client_secret'"
echo "  export TSG_ID='your_tsg_id'"
echo "  python web_app.py"
echo ""
echo "To run the CLI version:"
echo "  source venv/bin/activate"
echo "  export MODEL_SECURITY_CLIENT_ID='your_client_id'"
echo "  export MODEL_SECURITY_CLIENT_SECRET='your_client_secret'"
echo "  export TSG_ID='your_tsg_id'"
echo "  python main.py --cli"