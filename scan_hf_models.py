from huggingface_hub import HfApi
from model_security_client.api import ModelSecurityAPIClient

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