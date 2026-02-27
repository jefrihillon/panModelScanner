import os
import requests
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
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
load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
airs_api_key = os.getenv('PANW_AIRS_API_KEY')

airs_base_url = "https://service.api.aisecurity.paloaltonetworks.com"
scan_endpoint = f"{airs_base_url}/v1/scan"

headers = {
    "Content-Type": "application/json",
    "x-pan-token": airs_api_key  # Prisma AIRS scan API uses x-pan-token for API key
}

openai = OpenAI()
MODEL = 'gpt-4.1-mini'

system_message = "You are a helpful assistant"
def prompt_security(prompt):
    payload = {
        "prompt": prompt,
        "metadata": {
        "app_user": "example_user",
        "session_id": "session_xyz"
        }
    }
    response = requests.post(scan_endpoint, headers=headers, json=payload)
    if response.ok:
        try:
            data = response.json()
            print(json.dumps(data, indent=2))
        except json.JSONDecodeError:
            print("Failed to parse JSON response.")
    else:
        print(f"Error scanning prompt: {response.status_code} {response.text}")


def chat(message, history):
    history = [{"role":h["role"], "content":h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    prompt_security(message)
    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response

gr.ChatInterface(fn=chat).launch()