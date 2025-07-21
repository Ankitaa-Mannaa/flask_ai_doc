from chromadb import Client
from ai.embedder import embed_text
import numpy as np
import chromadb
from chromadb import EphemeralClient

chroma_client = EphemeralClient()

# Create a collection
chunk_collection = chroma_client.get_or_create_collection(name="document_chunks")
users_collection = chroma_client.get_or_create_collection(name="users")
documents_collection = chroma_client.get_or_create_collection(name="documents")
logs_collection = chroma_client.get_or_create_collection(name="logs")

__all__ = ['store_chunks', 'search_chunks', 'logs_collection']

def store_chunks(text, doc_id):
    splits = [text[i:i+500] for i in range(0, len(text), 500)]

    ids = []
    embeddings = []
    metadatas = []
    documents = []

    for idx, chunk_text in enumerate(splits):
        embedding = embed_text(chunk_text)
        ids.append(f"{doc_id}_{idx}")
        embeddings.append(embedding)
        metadatas.append({"doc_id": doc_id})
        documents.append(chunk_text)

    # Add to collection
    chunk_collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents
    )

    return [{"id": ids[i], "text": documents[i], "embedding": embeddings[i]} for i in range(len(ids))]


def search_chunks(query):
    query_embedding = embed_text(query)

    results = chunk_collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    matches = []
    for id_, doc, dist, meta in zip(
            results['ids'][0],
            results['documents'][0],
            results['distances'][0],
            results['metadatas'][0]
    ):
        matches.append({
            "id": id_,
            "text": doc,
            "score": 1 - dist, 
            "metadata": meta
        })

    return matches
