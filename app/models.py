from chromadb import Client
from datetime import datetime, timezone
import uuid
import chromadb
from chromadb.config import Settings, DEFAULT_TENANT, DEFAULT_DATABASE

chroma_client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE
)

# Collections
users_collection = chroma_client.get_or_create_collection(name="users")
documents_collection = chroma_client.get_or_create_collection(name="documents")
logs_collection = chroma_client.get_or_create_collection(name="logs")

# ---------- USER ----------
def add_user(name, email, password_hash, role='user'):
    user_id = str(uuid.uuid4())
    users_collection.add(
        ids=[user_id],
        metadatas=[{
            'name': name,
            'email': email,
            'password_hash': password_hash,
            'role': role
        }],
        documents=[email]
    )
    return user_id

def get_user_by_email(email):
    users = users_collection.get()
    for uid, meta in zip(users['ids'], users['metadatas']):
        if meta.get('email') == email:
            return uid, meta
    return None, None

def update_user_role(user_id, new_role):
    users_collection.update(
        ids=[user_id],
        metadatas=[{'role': new_role}]
    )

# ---------- DOCUMENT ----------
def add_document(filename, user_id):
    doc_id = str(uuid.uuid4())
    documents_collection.add(
        ids=[doc_id],
        metadatas=[{
            'filename': filename,
            'user_id': user_id,
            'upload_time': datetime.now(timezone.utc).isoformat()
        }],
        documents=[filename]
    )
    return doc_id

def get_documents_by_user(user_id):
    docs = documents_collection.get()
    return [
        {
            'filename': meta.get('filename'),
            'upload_time': meta.get('upload_time')
        }
        for meta in docs['metadatas'] if meta.get('user_id') == user_id
    ]

# ---------- LOGGING ----------
def log_action(user_id, action):
    logs_collection.add(
        ids=[str(uuid.uuid4())],
        metadatas=[{
            'user_id': user_id,
            'action': action,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }],
        documents=[action]
    )

def get_all_logs():
    logs = logs_collection.get()
    return [{
        'user_id': meta.get('user_id'),
        'action': meta.get('action'),
        'timestamp': meta.get('timestamp')
    } for meta in logs['metadatas']]
