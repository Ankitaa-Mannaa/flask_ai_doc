from flask import Blueprint, request, jsonify, abort
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

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
            if not user or user['role'] != required_role:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator
