from sentence_transformers import SentenceTransformer
<<<<<<< HEAD
import os


# Force Hugging Face model cache to a local folder
os.environ["TRANSFORMERS_CACHE"] = "./hf_cache"
os.environ["HF_HOME"] = "./hf_cache"
os.environ["HF_DATASETS_CACHE"] = "./hf_cache"
os.environ["HF_MODULES_CACHE"] = "./hf_cache"
os.environ["HF_METRICS_CACHE"] = "./hf_cache"


# Safe model load
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_text(text):
    return embedder.encode(text).tolist()
=======

embedder = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    return embedder.encode(text).tolist()
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05
