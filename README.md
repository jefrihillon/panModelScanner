# Hugging Face Model Security Scanner

This application provides a web interface for scanning Hugging Face models for security vulnerabilities using the Palo Alto Networks Model Security API. Users must provide a security group UUID to specify which models to scan based on their security group settings.

## Features

- Scan specific Hugging Face models by URL
- Scan multiple models using advanced search criteria from the Hugging Face API
- User-friendly web interface with forms instead of command-line prompts

## Advanced Search Criteria

The application supports the following search criteria for finding models:
- **Task Type (pipeline_tag)**: Filter by specific ML task (e.g., text-classification, image-classification)
- **Author**: Filter by model author/organization
- **Model Name**: Search for specific model names
- **General Search**: Search across all model fields
- **Trained Dataset**: Filter by dataset the model was trained on
- **Library**: Filter by foundational library (e.g., transformers, pytorch)
- **Language**: Filter by language supported by the model
- **Tags**: Filter by additional tags
- **Sort Options**: Sort by relevance, last modified, downloads, or likes
- **Sort Direction**: Ascending or descending order

## Installation

### Option 1: Manual Installation
1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or if using uv:
   ```bash
   uv pip install -r pyproject.toml
   ```

2. Set up the required environment variables:
   ```bash
   export MODEL_SECURITY_CLIENT_ID="your_client_id"
   export MODEL_SECURITY_CLIENT_SECRET="your_client_secret"
   export TSG_ID="your_tsg_id"
   ```

### Option 2: Using Build Script
1. Run the build script:
   ```bash
   ./build.sh
   ```

2. Set up the required environment variables:
   ```bash
   export MODEL_SECURITY_CLIENT_ID="your_client_id"
   export MODEL_SECURITY_CLIENT_SECRET="your_client_secret"
   export TSG_ID="your_tsg_id"
   ```

### Option 3: Using Environment File
1. Create an .env file with your actual values:
   ```bash
   # Update the values in .env file
   MODEL_SECURITY_CLIENT_ID="your_client_id"
   MODEL_SECURITY_CLIENT_SECRET="your_client_secret"
   TSG_ID="your_tsg_id"
   ```

2. Source the environment file:
   ```bash
   source .env
   ```

### Option 4: Docker Installation
With Docker installed, you can build and run the application using either the Dockerfile directly or docker-compose. The Dockerfile expects to find a .env file with the required environment variables configured with your specific credentials. Make sure to update the .env file with your actual credentials before running the Docker containers.

## Usage

### Direct Execution
1. Run the web application:
   ```bash
   python web_app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. When using the web interface, you'll need to provide a Security Group UUID in the new input field at the top of the page. This UUID determines which models will be scanned based on your security group settings.

### Using Run Script
1. Set up environment variables (see Installation section)

2. Run the application:
   ```bash
   ./run.sh
   ```

3. Open your browser and navigate to `http://localhost:5000`

4. When using the web interface, you'll need to provide a Security Group UUID in the new input field at the top of the page.

### Command-Line Interface
To use the CLI version:
```bash
python main.py --cli
```

When running the CLI, you'll be prompted to enter a Security Group UUID before proceeding with the scan.

### Docker Execution
1. Update the .env file with your actual MODEL_SECURITY_CLIENT_ID, MODEL_SECURITY_CLIENT_SECRET, and TSG_ID values

2. Build and run with Docker:
   ```bash
   docker build -t hf-model-scanner .
   docker run -p 5000:5000 --env-file .env hf-model-scanner
   ```

3. Open your browser and navigate to `http://localhost:5000`

4. When using the web interface, you'll need to provide a Security Group UUID in the new input field at the top of the page.

### Docker Compose Execution
1. Update the .env file with your actual MODEL_SECURITY_CLIENT_ID, MODEL_SECURITY_CLIENT_SECRET, and TSG_ID values

2. Run with docker-compose:
   ```bash
   docker-compose up -d
   ```

3. Open your browser and navigate to `http://localhost:5000`

4. When using the web interface, you'll need to provide a Security Group UUID in the new input field at the top of the page.

Note: The Docker image now loads environment variables from the .env file, so you can modify your credentials there instead of setting them as environment variables in your shell.

## How It Works

The application uses the Hugging Face Hub API to discover models and the Palo Alto Networks Model Security API to scan them for potential security issues.

Key features include:
- Scan specific Hugging Face models by URL
- Scan multiple models using advanced search criteria from the Hugging Face API
- User-friendly web interface with forms instead of command-line prompts
- Mandatory Security Group UUID input to customize which models are scanned based on security group settings

The web interface collects user input through HTML forms and displays the scan results in an easy-to-read format. Users must provide a Security Group UUID which determines which models will be scanned based on their security group settings.