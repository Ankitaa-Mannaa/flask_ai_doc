<<<<<<< HEAD
from chromadb import Client
from ai.embedder import embed_text
import numpy as np
import chromadb
from chromadb.config import Settings, DEFAULT_TENANT, DEFAULT_DATABASE

chroma_client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE
)

# Create a collection
collection = chroma_client.get_or_create_collection(name="document_chunks")
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
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents
    )

    return [{"id": ids[i], "text": documents[i], "embedding": embeddings[i]} for i in range(len(ids))]


def search_chunks(query):
    query_embedding = embed_text(query)

    results = collection.query(
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
=======
from . import mongo
from ai.embedder import embed_text
import numpy as np
from bson import ObjectId

def store_chunks(text, doc_id):
    """
    Splits `text` into 500-character chunks,
    embeds each chunk, stores them in MongoDB.
    """
    # Delete existing chunks for this doc_id to avoid duplicate key errors
    mongo.db.chunks.delete_many({'doc_id': ObjectId(doc_id)})

    chunks = []
    splits = [text[i:i+500] for i in range(0, len(text), 500)]

    for chunk_text in splits:
        embedding = embed_text(chunk_text)
        chunk_doc = {
            'doc_id': ObjectId(doc_id),
            'text': chunk_text,
            'embedding': embedding  # Should be JSON serializable list
        }
        # Ensure no _id field is present
        chunk_doc.pop('_id', None)
        chunks.append(chunk_doc)

    if chunks:
        mongo.db.chunks.insert_many(chunks)

    return chunks  # Important: Return the list for user.py to reuse


def search_chunks(query):
    """
    Embeds the query, computes cosine similarity with all chunks in MongoDB,
    returns top 5 most similar.
    """
    query_embedding = embed_text(query)

    chunks = list(mongo.db.chunks.find({}))
    scores = []

    for chunk in chunks:
        chunk_embedding = chunk['embedding']
        score = cosine_sim(query_embedding, chunk_embedding)
        scores.append({
            'id': str(chunk['_id']),
            'text': chunk['text'],
            'score': score
        })

    top = sorted(scores, key=lambda x: x['score'], reverse=True)[:5]
    return top


def cosine_sim(vec1, vec2):
    """
    Computes cosine similarity between two vectors.
    """
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05
