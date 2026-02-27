import os
import requests
import json
from pprint import pprint
import aisecurity
from aisecurity.generated_openapi_client.models.ai_profile import AiProfile
# IMPORTANT: For traditional (non-asyncio), import Scanner from aisecurity.scan.inline.scanner
from aisecurity.scan.inline.scanner import Scanner
from aisecurity.scan.models.content import Content

AI_PROFILE_NAME = "ai-sec-security"
API_KEY = os.getenv("PANW_AI_SEC_API_KEY")

# Initialize the SDK with your API Key
aisecurity.init(api_key=API_KEY)

# Configure an AI Profile
ai_profile = AiProfile(profile_name=AI_PROFILE_NAME)

CLIENT_ID = os.getenv("PANW_CLIENT_ID")
CLIENT_SECRET = os.getenv("PANW_CLIENT_SECRET")
TOKEN_URL = os.getenv("PANW_TOKEN_URL")

def get_access_token() -> str:
    print(TOKEN_URL)
    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )
    response.raise_for_status()
    token_data = response.json()
    return token_data["access_token"]

access_token = get_access_token()
print("Access token acquired")