# Hugging Face Model Security Scanner

This application provides a web interface for scanning Hugging Face models for security vulnerabilities using the Palo Alto Networks Model Security API. Users must provide a security group UUID to specify which models to scan based on their security group settings.

Please see AI Model Scanning documentation at: https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security

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
1. Set up the required environment variables or create and source .env file:
   ```bash
   export MODEL_SECURITY_CLIENT_ID="your_client_id"
   export MODEL_SECURITY_CLIENT_SECRET="your_client_secret"
   export TSG_ID="your_tsg_id"
   ```
2. Install AI Model Security.  See: https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/install-ai-model-security

3. Install remaining required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or if using uv:
   ```bash
   uv pip install -r pyproject.toml
   ```

### Option 2: Using Build Script
1. Set up the required environment variables or create and source .env:
   ```bash
   export MODEL_SECURITY_CLIENT_ID="your_client_id"
   export MODEL_SECURITY_CLIENT_SECRET="your_client_secret"
   export TSG_ID="your_tsg_id"
   ```

1. Run the build script:
   ```bash
   ./build.sh
   ```

### Option 3: Docker Installation
With Docker installed, you can build and run the application using either the Dockerfile directly or docker compose. The Dockerfile uses BuildKit secrets to securely handle environment variables during the build process, preventing credentials from being copied into the container image. Make sure to have a .env file with your actual credentials before building the Docker image.

## Usage

### Direct Execution
1. Run the web application:
   ```bash
   python web_app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. When using the web interface, you'll need to provide the Security Group UUID (See: https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/scanning-models for info on Security Group UUIDs) into the input field at the top of the page. This UUID determines the security group settings.

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
1. Create individual secret files with your credentials:
   ```bash
   # You can either extract values from .env file:
   ./extract_secrets.sh

   # Or create the files manually:
   echo "your_client_id" > id.txt
   echo "your_client_secret" > secret.txt
   echo "your_tsg_id" > tsg.txt
   ```

2. Build and run with Docker using BuildKit secrets:
   ```bash
   # Enable BuildKit (if docker version < 23.x.x)
   export DOCKER_BUILDKIT=1

   # Build with secrets (credentials are NOT stored in the image)
   docker build -t hf-model-scanner \
     --secret id=id,src=id.txt \
     --secret id=secret,src=secret.txt \
     --secret id=tsg,src=tsg.txt \
     .

   # Run with environment variables (these are needed at runtime)
   docker run -p 5000:5000 --env-file .env hf-model-scanner
   ```

3. Open your browser and navigate to `http://localhost:5000`

4. When using the web interface, you'll need to provide a Security Group UUID in the new input field at the top of the page.

Note: During the build process, BuildKit secrets are used to authenticate with the model security service, but these secrets are NOT stored in the final image. Runtime environment variables are provided separately via the --env-file flag.

### Docker Compose Execution
1. Create individual secret files with your credentials:
   ```bash
   # You can either extract values from .env file:
   ./extract_secrets.sh

   # Or create the files manually:
   echo "your_client_id" > id.txt
   echo "your_client_secret" > secret.txt
   echo "your_tsg_id" > tsg.txt
   ```

2. Run with docker-compose:
   ```bash
   # Enable BuildKit
   export DOCKER_BUILDKIT=1

   # Build with secrets (credentials are NOT stored in the image)
   docker-compose build

   # Run with environment variables
   docker-compose up -d
   ```

3. Open your browser and navigate to `http://localhost:5000`

4. When using the web interface, you'll need to provide a Security Group UUID in the new input field at the top of the page.

Note: During the build process, BuildKit secrets are used to authenticate with the model security service, but these secrets are NOT stored in the final image. Runtime environment variables are provided separately via the env_file directive in compose.yml.

## How It Works

The application uses the Hugging Face Hub API to discover models and the Palo Alto Networks Model Security API to scan them for potential security issues.

Key features include:
- Scan specific Hugging Face models by URL
- Scan multiple models using advanced search criteria from the Hugging Face API
- User-friendly web interface with forms instead of command-line prompts
- Mandatory Security Group UUID input to customize which models are scanned based on security group settings

The web interface collects user input through HTML forms and displays the scan results in an easy-to-read format. Users must provide a Security Group UUID which determines which models will be scanned based on their security group settings.