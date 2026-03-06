# PAN Model Security Scanner UI

<img width="1176" height="841" alt="Screenshot 2026-03-05 at 2 20 01 PM" src="https://github.com/user-attachments/assets/0afb4391-6335-4d24-996d-753d43b937f9" />

<img width="1174" height="844" alt="Screenshot 2026-03-05 at 2 21 58 PM" src="https://github.com/user-attachments/assets/8838c8fb-4ecb-4426-a991-f625d22c122e" />

<img width="1151" height="191" alt="Screenshot 2026-03-05 at 2 34 32 PM" src="https://github.com/user-attachments/assets/90ca16cd-937d-4240-a3d3-e38453c1702b" />

See AI Model Scanning documentation at: https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security

### Scanning Methods

1. **Hugging Face Models**: Scan models directly from Hugging Face Hub using URLs or search criteria
2. **Local Models**: Upload model files directly through the web interface for scanning
3. **Object Storage Models**: Scan models stored in cloud block storage (S3, GCS, Azure)

Each scan supports labeling for better organization and outcome tracking.  See: https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/organize-security-scans-with-custom-labels

## How It Works

The application provides a browser-based UI for the Palo Alto Networks Model Scanning Client to use the Hugging Face Hub API, local model storage and/or public block storage to scan models for potential security risks.

## Features

- Scan specific Hugging Face models by URL
- Scan multiple models using available search criteria published via the HuggingFace API
- Scan local model files with direct upload
- Scan models hosted in cloud object storage (Amazon S3, Google Cloud Storage, Azure Blob Storage)
- User-friendly web interface
- Responsive design that works on desktop and mobile devices
- Real-time feedback with loading indicators and ALLOWED/BLOCKED outcomes

## Advanced Search Criteria

The application supports the following search criteria for finding Hugging Face models:
- **Task Type (pipeline_tag)**: Filter by specific ML task (e.g., text-classification, image-classification, text-to-speech...)
- **Author**: Filter by model author/organization
- **Model Name**: Search for specific model names
- **General Search**: Search across available model fields
- **Trained Dataset**: Filter by the dataset the model was trained on
- **Library**: Filter by foundational library (e.g., transformers, pytorch, etc)
- **Language**: Filter by language supported by the model
- **Tags**: Filter by tags
- **Sort Options**: Sort by relevance, last modified, downloads, or likes
- **Sort Direction**: Ascending/Descending

## Required
- **User must provide a Security Group UUID** - maps to the Model Security Group scan settings.

### Installation

## Kubernetes/Docker Deployment (Recommended)

To deploy the application to a Kubernetes cluster or docker host:

#Kubernetes
1. Ensure you have kubectl configured to access your cluster

2. Create a Kubernetes deployment or pod yaml file and set your individual environment variables:
   - MODEL_SECURITY_CLIENT_ID
   - MODEL_SECURITY_CLIENT_SECRET
   - TSG_ID

   Create a `deployment.yaml` or `pod.yaml` file to pull the image: jefrihillon/pan-model-scanner-ui:version.  Add your individual model scanner credentials as environment variables or kubernetes secrets:
   ```yaml
   env:
   - name: MODEL_SECURITY_CLIENT_ID
     value: "your_client_id"
   - name: MODEL_SECURITY_CLIENT_SECRET
     value: "your_client_secret"
   - name: TSG_ID
     value: "your_tsg_id"
   ```

3. Apply the Kubernetes manifest(s):
   ```bash
   kubectl apply -f deployment.yaml service.yaml ...
   ```

Note: For production deployments, consider using Kubernetes secrets to manage sensitive environment variables rather than hardcoding them as local environment variables.

#Docker/Compose
1. ```
   docker run -p 5000:5000 --env-file .env pan-model-scanner-ui
   ```
   or:
   ```
   docker-compose up -d
   ```

## Option 2: Use Build Script
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

## Option 3: Manual Installation
1. Set up the required environment variables or create and source .env file:
   ```bash
   export MODEL_SECURITY_CLIENT_ID="your_client_id"
   export MODEL_SECURITY_CLIENT_SECRET="your_client_secret"
   export TSG_ID="your_tsg_id"
   ```

2. Install AI Model Security.  See: https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/install-ai-model-security

3. Install remaining dependencies:
   ```bash
   pip install -r requirements.txt 
   ```
   or:
   ```bash
   uv pip install -r pyproject.toml
   ```

### Usage

## Connect to hosted Kubernetes/Docker service
1. http(s)://pan-model-scanner-ui-service(:5000)
   
## Direct Execution
1. Run the web application:
   ```bash
   python web_app.py
   ```

2. `http://localhost:5000`

## Use Run Script
1. Set up environment variables

2. Use run script:
   ```bash
   ./run.sh
   ```

3. `http://localhost:5000`

## Command-Line Interface
```bash
python main.py --cli
```
CLI prompts user for Security Group UUID


### Customize -> repackage
1. Create individual secret files with your credentials:
   ```bash
   # You can either extract values from .env file:
   ./extract_secrets.sh

   # Or create the files manually:
   echo "your_client_id" > id.txt
   echo "your_client_secret" > secret.txt
   echo "your_tsg_id" > tsg.txt
   ```

2. Build and run with Docker secrets:
   ```bash
   # Enable BuildKit (if docker version < 23.x.x)
   export DOCKER_BUILDKIT=1

   docker build -t pan-model-scanner-ui \
     --secret id=id,src=id.txt \
     --secret id=secret,src=secret.txt \
     --secret id=tsg,src=tsg.txt \
     .

   # Apply environment variables at runtime
   docker run -p 5000:5000 --env-file .env pan-model-scanner-ui
   ```
   or:
   ```
   docker-compose up -d
   ```

3. `http://localhost:5000`

4. When using the web interface, you'll need to provide a Security Group UUID in the new input field at the top of the page.
