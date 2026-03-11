# PAN Model Security Scanner UI

<img width="1176" height="841" alt="Screenshot 2026-03-05 at 2 20 01 PM" src="https://github.com/user-attachments/assets/0afb4391-6335-4d24-996d-753d43b937f9" />

<img width="1174" height="844" alt="Screenshot 2026-03-05 at 2 21 58 PM" src="https://github.com/user-attachments/assets/8838c8fb-4ecb-4426-a991-f625d22c122e" />

[Palo Alto Networks AI Model Scanning docs](https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security)

## Purpose
The application serves three purposes:
  1. **Bypass the [installation steps](https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security) required to enable the Model Scanning software.**
  2. **Immediately provide a user with all available search criteria when scanning open-source models via the [HuggingFace API Client](https://huggingface.co/docs/huggingface_hub/en/package_reference/hf_api).**
  3. Link scan individual results to Strata Cloud Manager for faster Model Scanning Group configuration modifications.
     
## Scan Methods
1. **Hugging Face Models**: Scan models directly from Hugging Face Hub using URLs or search criteria
2. **Local Models**: Upload model files directly through the web interface for scanning
3. **Object Storage Models**: Scan models stored in cloud block storage (S3, GCS, Azure)

Each scan supports [labeling](https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/organize-security-scans-with-custom-labels) for better organization and outcome tracking.


## HuggingFace Search Criteria
The following search criteria are searchable criteria when assessing risks associated with open-source HuggingFace models:
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
- **User must provide a Security Group UUID** - which maps to the [Model Security Group](https://stratacloudmanager.paloaltonetworks.com/ai-security/model-security/security-groups) scan settings.

# Installation

## Option 1: Kubernetes/Docker Deployment (Recommended)

## Kubernetes

2. Create a `deployment.yaml` or `pod.yaml` file (see example deployment.yaml) to pull image: jefrihillon/pan-model-scanner-ui:version.  Add your model scanner credentials as environment variables or Kubernetes secrets at runtime.
   **For production deployments, consider using more secure Kubernetes secrets over sensitive environment variables**
   ```yaml
   env:
   - name: MODEL_SECURITY_CLIENT_ID
     value: "your_client_id"
   - name: MODEL_SECURITY_CLIENT_SECRET
     value: "your_client_secret"
   - name: TSG_ID
     value: "your_tsg_id"
   ```

4. Apply the Kubernetes manifest(s):
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

Known Bugs
 - When hosting the application from a Kubernetes server and have issued a certificate via cert-manager, scans still successfully run, but the output from the scan has an html bug.  
