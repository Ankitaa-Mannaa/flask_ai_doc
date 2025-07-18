import requests
<<<<<<< HEAD
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
=======

OPENROUTER_API_KEY = "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"
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_answer(context, question):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-guard-4-12b",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {context}\nQuestion: {question}\nAnswer:"}
        ]
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
