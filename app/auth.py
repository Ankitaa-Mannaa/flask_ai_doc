from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from bcrypt import hashpw, gensalt, checkpw
from functools import wraps
import uuid
from chromadb import EphemeralClient

chroma_client = EphemeralClient()

users_collection = chroma_client.get_or_create_collection(name="users")
auth_bp = Blueprint('auth', __name__)

# Store user in Chroma
def store_user(email, name, password_hash):
    user_id = str(uuid.uuid4())
    users_collection.add(
        ids=[user_id],
        metadatas=[{
            "email": email,
            "name": name,
            "password_hash": password_hash,
            "role": "user"
        }],
        documents=[email]
    )
    return user_id

# Role check
def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user_data = users_collection.get()
            user_meta = next((m for i, m in zip(user_data['ids'], user_data['metadatas']) if i == user_id), None)

            if not user_meta or user_meta.get("role") != required_role:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Signup
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed = hashpw(data['password'].encode(), gensalt()).decode()
    all_users = users_collection.get()
    role = 'admin' if not all_users['ids'] else 'user'  # First user is Admin

    user_id = str(uuid.uuid4())
    users_collection.add(
        ids=[user_id],
        metadatas=[{
            'email': data['email'],
            'name': data['name'],
            'password_hash': hashed,
            'role': role
        }],
        documents=[data['email']]
    )
    token = create_access_token(identity=user_id)
    return jsonify({'access_token': token}), 201

# Login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    all_users = users_collection.get()
    for user_id, meta in zip(all_users["ids"], all_users["metadatas"]):
        if meta["email"] == data["email"] and checkpw(data["password"].encode('utf-8'), meta["password_hash"].encode('utf-8')):
            token = create_access_token(identity=user_id)
            return jsonify({'access_token': token}), 200

    return jsonify({'msg': 'Invalid credentials'}), 401

# Profile
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    all_users = users_collection.get()
    for id_, meta in zip(all_users["ids"], all_users["metadatas"]):
        if id_ == user_id:
            return jsonify({
                'id': id_,
                'name': meta['name'],
                'email': meta['email'],
                'role': meta['role']
            })

    return jsonify({'msg': 'User not found'}), 404
