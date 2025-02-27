import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()  # Load variables from .env

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def post_to_llm(message):
    print(message)
    return requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
                "model": "deepseek/deepseek-r1-distill-llama-8b",
                "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
        })
    )