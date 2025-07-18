from flask import Blueprint, request, jsonify, abort
<<<<<<< HEAD
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from chromadb import PersistentClient
from chromadb.config import Settings, DEFAULT_TENANT, DEFAULT_DATABASE
from bcrypt import hashpw, gensalt, checkpw
from functools import wraps
import uuid

# Setup Chroma client
chroma_client = PersistentClient(
    path="./chroma_db",
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE
)

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
=======
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
)
from bson import ObjectId
import bcrypt

from . import mongo

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    # Check if user already exists
    existing_user = mongo.db.users.find_one({'email': data['email']})
    if existing_user:
        return jsonify({'msg': 'User already exists'}), 400

    # Insert new user
    user = {
        'name': data['name'],
        'email': data['email'],
        'password_hash': hashed,
        'role': 'user'
    }
    result = mongo.db.users.insert_one(user)

    token = create_access_token(identity=str(result.inserted_id))
    return jsonify({'access_token': token}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({'email': data['email']})

    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password_hash']):
        token = create_access_token(identity=str(user['_id']))
        return jsonify({'access_token': token}), 200

    return jsonify({'msg': 'Invalid credentials'}), 401

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})

    if not user:
        return jsonify({'msg': 'User not found'}), 404

    return jsonify({
        'id': str(user['_id']),
        'name': user['name'],
        'email': user['email'],
        'role': user['role']
    })


from functools import wraps

>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05
def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
<<<<<<< HEAD
            user_data = users_collection.get()
            user_meta = next((m for i, m in zip(user_data['ids'], user_data['metadatas']) if i == user_id), None)

            if not user_meta or user_meta.get("role") != required_role:
=======
            user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
            if not user or user['role'] != required_role:
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator
<<<<<<< HEAD

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
=======
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05
