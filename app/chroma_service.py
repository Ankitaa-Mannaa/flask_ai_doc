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
            'embedding': embedding 
        }
        
        
        chunk_doc.pop('_id', None)
        chunks.append(chunk_doc)

    if chunks:
        mongo.db.chunks.insert_many(chunks)

    return chunks 


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
