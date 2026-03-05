from huggingface_hub import HfApi
from model_security_client.api import ModelSecurityAPIClient
import os
import tempfile
import shutil
import boto3
from google.cloud import storage
from azure.storage.blob import BlobServiceClient

HF_URI="https://huggingface.co/"
api= HfApi()

# Initialize the client
client = ModelSecurityAPIClient(
    base_url="https://api.sase.paloaltonetworks.com/aims"
)

def scan_hf_model(model, security_group_uuid, env_label="default"):
    """Scan a single Hugging Face model for security vulnerabilities"""
    try:
        model_version = api.model_info(model.modelId).sha
        result = client.scan(
                security_group_uuid=security_group_uuid,
                model_uri=HF_URI + model.modelId,
                model_version=model_version,
                labels={ "env": env_label }
        )
        return f"{model.modelId} scan completed: {result.eval_outcome}"
    except Exception as e:
        return f"{model.modelId} scan failed: {str(e)}"

def scan_local_model(model_path, security_group_uuid, env_label="default", model_name="", model_version=""):
    """Scan a local model file for security vulnerabilities"""
    try:
        # Validate that the model path exists
        if not os.path.exists(model_path):
            return f"Local model scan failed: Model path '{model_path}' does not exist"

        # Scan the local model
        result = client.scan(
                security_group_uuid=security_group_uuid,
                model_path=model_path,
                model_name=model_name if model_name else "local-model",
                model_version=model_version if model_version else "1.0",
                labels={ "env": env_label }
        )
        return f"Local model scan completed: {result.eval_outcome}"
    except Exception as e:
        return f"Local model scan failed: {str(e)}"

def download_from_s3(s3_uri, temp_dir):
    """Download a model from S3 to a temporary directory"""
    try:
        # Parse S3 URI
        if not s3_uri.startswith("s3://"):
            raise ValueError("Invalid S3 URI format")

        # Extract bucket and key
        s3_parts = s3_uri[5:].split("/", 1)
        bucket_name = s3_parts[0]
        key = s3_parts[1] if len(s3_parts) > 1 else ""

        # Initialize S3 client
        s3_client = boto3.client('s3')

        # Create local path
        local_path = os.path.join(temp_dir, os.path.basename(key) if key else "model")

        # Download the file
        s3_client.download_file(bucket_name, key, local_path)

        return local_path
    except Exception as e:
        raise Exception(f"Failed to download from S3: {str(e)}")

def download_from_gcs(gcs_uri, temp_dir):
    """Download a model from Google Cloud Storage to a temporary directory"""
    try:
        # Parse GCS URI
        if not gcs_uri.startswith("gs://"):
            raise ValueError("Invalid GCS URI format")

        # Extract bucket and blob
        gcs_parts = gcs_uri[5:].split("/", 1)
        bucket_name = gcs_parts[0]
        blob_name = gcs_parts[1] if len(gcs_parts) > 1 else ""

        # Initialize GCS client
        client = storage.Client()

        # Get the bucket and blob
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Create local path
        local_path = os.path.join(temp_dir, os.path.basename(blob_name) if blob_name else "model")

        # Download the file
        blob.download_to_filename(local_path)

        return local_path
    except Exception as e:
        raise Exception(f"Failed to download from GCS: {str(e)}")

def download_from_azure(azure_uri, temp_dir):
    """Download a model from Azure Blob Storage to a temporary directory"""
    try:
        # Parse Azure URI
        if not azure_uri.startswith("https://") or ".blob.core.windows.net" not in azure_uri:
            raise ValueError("Invalid Azure Blob Storage URI format")

        # Extract account, container, and blob
        # Format: https://account.blob.core.windows.net/container/blob
        uri_parts = azure_uri.split("/")
        account_name = uri_parts[2].split(".")[0]
        container_name = uri_parts[3]
        blob_name = "/".join(uri_parts[4:])

        # Initialize Azure client
        # Note: This requires Azure credentials to be configured
        blob_service_client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=None  # Will use default credentials
        )

        # Get blob client
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )

        # Create local path
        local_path = os.path.join(temp_dir, os.path.basename(blob_name) if blob_name else "model")

        # Download the file
        with open(local_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        return local_path
    except Exception as e:
        raise Exception(f"Failed to download from Azure: {str(e)}")

def download_from_https(https_uri, temp_dir):
    """Download a model from HTTPS URL to a temporary directory"""
    try:
        import requests

        # Create local path
        filename = os.path.basename(https_uri.split("?")[0]) or "model"
        local_path = os.path.join(temp_dir, filename)

        # Download the file
        response = requests.get(https_uri, stream=True)
        response.raise_for_status()

        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return local_path
    except Exception as e:
        raise Exception(f"Failed to download from HTTPS: {str(e)}")

def scan_storage_model(storage_uri, security_group_uuid, env_label="default", model_name="", model_version="", temp_path="/tmp"):
    """Scan a model from object storage for security vulnerabilities"""
    temp_dir = None
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp(dir=temp_path)

        # Download model based on URI type
        if storage_uri.startswith("s3://"):
            local_model_path = download_from_s3(storage_uri, temp_dir)
        elif storage_uri.startswith("gs://"):
            local_model_path = download_from_gcs(storage_uri, temp_dir)
        elif storage_uri.startswith("https://") and ".blob.core.windows.net" in storage_uri:
            local_model_path = download_from_azure(storage_uri, temp_dir)
        elif storage_uri.startswith("https://"):
            local_model_path = download_from_https(storage_uri, temp_dir)
        else:
            raise ValueError("Unsupported storage URI format")

        # Scan the downloaded model
        result = client.scan(
                security_group_uuid=security_group_uuid,
                model_path=local_model_path,
                model_uri=storage_uri,
                model_name=model_name if model_name else "storage-model",
                model_version=model_version if model_version else "1.0",
                labels={ "env": env_label }
        )

        return f"Storage model scan completed: {result.eval_outcome}"
    except Exception as e:
        return f"Storage model scan failed: {str(e)}"
    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

def scan_specific_model(model_url, security_group_uuid, env_label="default"):
    """Scan a specific model by URL"""
    try:
        model_info = api.model_info(model_url.replace(HF_URI, ""))
        return scan_hf_model(model_info, security_group_uuid, env_label)
    except Exception as e:
        return f"Failed to scan model: {str(e)}"

def scan_models_by_criteria(tag=None, author=None, model_name=None, search=None,
                           trained_dataset=None, library=None, language=None,
                           tags=None, limit=None, sort=None, direction=None,
                           security_group_uuid="715dab90-31ad-44f6-9fe2-dcef4335ec35",
                           env_label="default"):
    """Scan models based on various criteria from the Hugging Face API"""
    try:
        # Prepare filter parameters, only include non-None values
        filter_params = {}

        if tag:
            filter_params['pipeline_tag'] = tag
        if author:
            filter_params['author'] = author
        if model_name:
            filter_params['model_name'] = model_name
        if search:
            filter_params['search'] = search
        if trained_dataset:
            filter_params['trained_dataset'] = trained_dataset
        if library:
            filter_params['library'] = library
        if language:
            filter_params['language'] = language
        if tags:
            filter_params['tags'] = tags
        if limit:
            filter_params['limit'] = limit
        if sort:
            filter_params['sort'] = sort
        if direction:
            filter_params['direction'] = direction

        # Filter models based on criteria
        models = list(api.list_models(**filter_params))

        results = []
        for model in models:
            result = scan_hf_model(model, security_group_uuid, env_label)
            results.append(result)

        return results
    except Exception as e:
        return [f"Failed to scan models: {str(e)}"]

def run_scan():
    """Run the interactive command-line scanner"""
    security_group_uuid = input("Enter security group UUID (mandatory): ").strip()
    if not security_group_uuid:
        print("Security group UUID is required.")
        return

    env_label = input("Enter environment label (optional, press Enter for 'default'): ").strip()
    if not env_label:
        env_label = "default"

    model_url = input("If you have a specific Hugging Face model in mind, enter the full URL here (optional): ")
    if model_url:
        print(scan_specific_model(model_url, security_group_uuid, env_label))
    else:
        print("Enter search criteria (leave blank for no filter):")
        tag = input("Task Type (pipeline_tag): ").strip()
        author = input("Author: ").strip()
        model_name = input("Model Name: ").strip()
        search = input("General Search Term: ").strip()
        trained_dataset = input("Trained Dataset: ").strip()
        library = input("Library: ").strip()
        language = input("Language: ").strip()
        tags = input("Tags (comma-separated): ").strip()

        limit_str = input("Number of Models (optional): ").strip()
        limit = None
        if limit_str and limit_str.isdigit():
            limit = int(limit_str)

        # Only include non-empty parameters
        params = {}
        if tag:
            params['tag'] = tag
        if author:
            params['author'] = author
        if model_name:
            params['model_name'] = model_name
        if search:
            params['search'] = search
        if trained_dataset:
            params['trained_dataset'] = trained_dataset
        if library:
            params['library'] = library
        if language:
            params['language'] = language
        if tags:
            params['tags'] = tags
        if limit:
            params['limit'] = limit

        # Add security_group_uuid and env_label to params
        params['security_group_uuid'] = security_group_uuid
        params['env_label'] = env_label

        if not params:
            print("No search criteria provided. Scanning popular models...")

        results = scan_models_by_criteria(**params)
        for result in results:
            print(result)

if __name__ == "__main__":
    run_scan()