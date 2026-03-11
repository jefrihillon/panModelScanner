# PAN Model Security Scanner UI

<img width="1176" height="841" alt="Screenshot 2026-03-05 at 2 20 01 PM" src="https://github.com/user-attachments/assets/0afb4391-6335-4d24-996d-753d43b937f9" />

<img width="1174" height="844" alt="Screenshot 2026-03-05 at 2 21 58 PM" src="https://github.com/user-attachments/assets/8838c8fb-4ecb-4426-a991-f625d22c122e" />

[Palo Alto Networks AI Model Scanning docs](https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security)

## Scanning Methods

1. **Hugging Face Models**: Scan models directly from Hugging Face Hub using URLs or search criteria
2. **Local Models**: Upload model files directly through the web interface for scanning
3. **Object Storage Models**: Scan models stored in cloud block storage (S3, GCS, Azure)

Each scan supports [labeling](https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/organize-security-scans-with-custom-labels) for better organization and outcome tracking.

## What It Does

The application provides a browser-based UI for the Palo Alto Networks Model Scanning Client to use the Hugging Face Hub API, local model storage and/or public block storage to scan models for potential security risks.

## Features

- User-friendly web interface
- Scan specific Hugging Face models by URL
- Scan multiple models using available search criteria published via the HuggingFace API
- Scan local model files with direct upload
- Scan models hosted in cloud object storage (Amazon S3, Google Cloud Storage, Azure Blob Storage)
- Responsive design that works on desktop and mobile devices
- Real-time feedback with loading indicators and ALLOWED/BLOCKED outcomes

## Search Criteria

The application supports the following search criteria for finding Hugging Face models:
- **Task Type (pipeline_tag)**: Filter by specific ML task (e.g., text-classification, image-classification, text-to-speech...)
  - **Natural Language Processing:**
    - `text-classification` (alias `sentiment-analysis` available)
    - `token-classification` (alias `ner` available)
    - `question-answering`
    - `fill-mask`
    - `summarization`
    - `translation_xx_to_yy` and `translation`
    - `text2text-generation`
    - `text-generation`
    - `zero-shot-classification`
    - `table-question-answering`
    - `feature-extraction`
    - `conversational`
  - **Audio:**
    - `automatic-speech-recognition`
    - `audio-classification`
    - `text-to-audio` (alias `text-to-speech` available)
    - `zero-shot-audio-classification`
  - **Computer Vision:**
    - `image-classification`
    - `object-detection`
    - `image-segmentation`
    - `image-to-text`
    - `depth-estimation`
    - `video-classification`
    - `zero-shot-image-classification`
    - `zero-shot-object-detection`
    - `mask-generation`
    - `visual-question-answering`
    - `document-question-answering`
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

# Installation

## Option 1: Kubernetes/Docker Deployment (Recommended)

## Kubernetes

2. Create a `deployment.yaml` or `pod.yaml` file to pull image: jefrihillon/pan-model-scanner-ui:version.  Add your individual model scanner credentials as environment variables or Kubernetes secrets at runtime.  For production deployments, consider using more secure Kubernetes secrets over sensitive environment variables.
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

## Docker/Compose
1. Apply environment variables at runtime
   ```
   docker run -p 5000:5000 --env-file .env pan-model-scanner-ui
   ```
   or:
   
   ```
   docker compose up -d
   ```

## Option 2: Use Build Script
1. Set up required environment variables or create and source .env:
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
1. Set up required environment variables or create and source .env file:

2. Install AI Model Security.  See: https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/install-ai-model-security

3. Install remaining dependencies:
   ```bash
   pip install -r requirements.txt 
   ```
   or:
   
   ```bash
   uv pip install -r pyproject.toml
   ```

# Usage

## Connect to hosted Kubernetes/Docker service
1. http(s)://pan-model-scanner-ui-service(:5000)
   
## Direct Execution
1. Run web application:
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


# Customize -> repackage
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

   docker run -p 5000:5000 --env-file .env pan-model-scanner-ui
   or:
   docker compose up -d
   ```

<<<<<<< HEAD
## Current Known Bugs
 - if hosting on a kubernetes server and have issued a certificate via cert-manager, scans still successfully run, but the output from the scan has an html bug.  You will still see your scan results in Strata Cloud Manager.
=======
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

The web interface collects user input through HTML forms and displays the scan results in an easy-to-read format. Users must provide a Security Group UUID which determines which models will be scanned based on their security group settings.

### Scanning Methods

1. **Hugging Face Models**: Scan models directly from Hugging Face Hub using URLs or search criteria
2. **Local Models**: Upload model files directly through the web interface for scanning
3. **Object Storage Models**: Scan models stored in cloud storage services (S3, GCS, Azure, HTTPS)

Each scanning method supports custom model metadata (name, version) and environment labeling for better organization and tracking.  See: https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/organize-security-scans-with-custom-labels
>>>>>>> 77c0487 (commit on main)
