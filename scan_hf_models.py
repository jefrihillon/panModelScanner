from huggingface_hub import HfApi
from model_security_client.api import ModelSecurityAPIClient

HF_URI="https://huggingface.co/"
api= HfApi()

# Initialize the client
client = ModelSecurityAPIClient(
    base_url="https://api.sase.paloaltonetworks.com/aims"
)

tag = input("Enter the Hugging Face task type: ").lower()
author = input("Enter the Hugging Face author: ").lower()
limit = input("Enter the number of models to retrieve (optional): ")
limit = int(limit) if limit.isdigit() else None


# Filter for Automatic Speech Recognition models by OpenAI
models = list(api.list_models(
        pipeline_tag=tag,
        author=author,
        limit=limit
))

print(f"Total models found: {len(models)}")
for model in models:
    print(HF_URI+model.modelId)

    result = client.scan(
            security_group_uuid="44f4e8b4-19e4-4a2f-bff1-b9cff232ed1e",
            model_uri=HF_URI + model.modelId,
            labels={ "env": "j5k-testGroup1" }
    )

    print(f"{model.modelId} scan completed: {result.eval_outcome}")
