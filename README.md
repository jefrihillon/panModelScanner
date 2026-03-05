# PAN Model Security Scanner UI
<img width="1176" height="841" alt="Screenshot 2026-03-05 at 2 20 01 PM" src="https://github.com/user-attachments/assets/0afb4391-6335-4d24-996d-753d43b937f9" />

<img width="1174" height="844" alt="Screenshot 2026-03-05 at 2 21 58 PM" src="https://github.com/user-attachments/assets/8838c8fb-4ecb-4426-a991-f625d22c122e" />

<img width="1151" height="191" alt="Screenshot 2026-03-05 at 2 34 32 PM" src="https://github.com/user-attachments/assets/90ca16cd-937d-4240-a3d3-e38453c1702b" />


This application provides a web interface for scanning Hugging Face models, Local Models, or Object Storage for security vulnerabilities using the Palo Alto Networks Model Security API. Users must provide a security group UUID to specify which models to scan based on their security group settings.

Please see AI Model Scanning documentation at: https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security

## Features

- Scan specific Hugging Face models by URL
- Scan multiple models using advanced search criteria from the Hugging Face API
- Scan local model files with direct upload capability
- Scan models from cloud object storage (Amazon S3, Google Cloud Storage, Azure Blob Storage, HTTPS)
- User-friendly web interface with forms instead of command-line prompts
- Responsive design that works on desktop and mobile devices
- Real-time feedback with loading indicators and success/error notifications

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
With Docker installed, you can build and run the application using either the Dockerfile directly or docker compose. The Dockerfile uses BuildKit secrets to securely handle environment variables during the build process, preventing credentials from being copied into the container image if you make your own changes to the code and want to republish it to a public repo (dockerhub i.e.). You can put your own environment variables into a .env file and use ./extract_secrets.sh to secure them where only root can view and lauch the app with a simple 'docker compose up -d'.

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

   # Build with secrets
   docker build -t hf-model-scanner \
     --secret id=id,src=id.txt \
     --secret id=secret,src=secret.txt \
     --secret id=tsg,src=tsg.txt \
     .

   # Run with environment variables (needed at runtime for your own TSG, CLIENT_ID, and CLIENT_SECRET)
   docker run -p 5000:5000 --env-file .env hf-model-scanner
   ```

3. Open your browser and navigate to `http://localhost:5000`

4. When using the web interface, you'll need to provide a Security Group UUID in the new input field at the top of the page.

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
   # Run with environment variables
   docker-compose up -d
   ```

3. Open your browser and navigate to `http://localhost:5000`

4. When using the web interface, you'll need to provide a Security Group UUID in the new input field at the top of the page.

### Kubernetes Deployment

To deploy the application to a Kubernetes cluster:

1. Ensure you have kubectl configured to access your cluster

2. Update a Kubernetes deployment or pod yaml file with your environment model scanner environment variables:
   The deployment file includes environment variables for:
   - MODEL_SECURITY_CLIENT_ID
   - MODEL_SECURITY_CLIENT_SECRET
   - TSG_ID

   Create a `deployment.yaml` or `pod.yaml` file to pull the image: jefrihillon/pan-model-scanner-ui and within the pod spec for the image add the environment variables for your specific model scanner credentials:
   ```yaml
   env:
   - name: MODEL_SECURITY_CLIENT_ID
     value: "your_client_id_here"
   - name: MODEL_SECURITY_CLIENT_SECRET
     value: "your_client_secret_here"
   - name: TSG_ID
     value: "your_tsg_id_here"
   ```

3. Apply the Kubernetes manifest(s):
   ```bash
   kubectl apply -f deployment.yaml service.yaml ...
   ```

Note: For production deployments, consider using Kubernetes secrets to manage sensitive environment variables rather than hardcoding them in the deployment file.

## How It Works

The application uses the Hugging Face Hub API to discover models and the Palo Alto Networks Model Security API to scan them for potential security issues.

Key features include:
- Scan specific Hugging Face models by URL
- Scan multiple models using advanced search criteria from the Hugging Face API
- Scan local model files uploaded directly through the web interface
- Scan models stored in cloud object storage (S3, GCS, Azure Blob Storage, HTTPS)
- User-friendly web interface with forms instead of command-line prompts
- Mandatory Security Group UUID input to customize which models are scanned based on security group settings
- Dark theme interface with Palo Alto Networks brand colors (#FA582D orange and #0047BA blue)

The web interface collects user input through HTML forms and displays the scan results in an easy-to-read format. Users must provide a Security Group UUID which determines which models will be scanned based on their security group settings.

### Scanning Methods

1. **Hugging Face Models**: Scan models directly from Hugging Face Hub using URLs or search criteria
2. **Local Models**: Upload model files directly through the web interface for scanning
3. **Object Storage Models**: Scan models stored in cloud storage services (S3, GCS, Azure, HTTPS)

Each scanning method supports custom model metadata (name, version) and environment labeling for better organization and tracking.  See: https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/organize-security-scans-with-custom-labels
