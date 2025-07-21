import requests

# Your Hugging Face Space endpoint
HF_SPACE_URL = "https://Anki27-anki-embedder.hf.space/embed"

def embed_text(text):
    response = requests.post(
        HF_SPACE_URL,
        json={"text": text},
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 200:
        return response.json()["embedding"]
    else:
        raise Exception(f"Embedding request failed: {response.status_code} - {response.text}")
