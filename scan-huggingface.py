from model_security_client.api import ModelSecurityAPIClient

# Initialize the client
client = ModelSecurityAPIClient(
    base_url="https://api.sase.paloaltonetworks.com/aims"
)

result = client.scan(
    security_group_uuid="074dd9aa-9d3e-430e-9db6-5c891560ef55",
    model_uri="https://huggingface.co/soumildatta/mochi-lora",
    labels={ "env": "production" }
)

print(f"Scan completed: {result.eval_outcome}")