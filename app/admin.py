from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .auth import role_required
from .chroma_service import logs_collection, users_collection
import uuid
from datetime import datetime
import chromadb
from chromadb.config import Settings
from .chroma_service import chroma_client


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_users():
    users = users_collection.get()
    return jsonify([{
        'id': user_id,
        'name': meta.get('name'),
        'email': meta.get('email'),
        'role': meta.get('role')
    } for user_id, meta in zip(users['ids'], users['metadatas'])])

@admin_bp.route('/admin/assign-role', methods=['POST'])
@jwt_required()
@role_required('admin')
def assign_role():
    data = request.get_json()
    user_id = data['user_id']
    new_role = data['new_role']

    users_collection.update(
        ids=[user_id],
        metadatas=[{'role': new_role}]
    )

    logs_collection.add(
        ids=[str(uuid.uuid4())],
        metadatas=[{
            'user_id': user_id,
            'action': f'Role changed to {new_role}',
            'timestamp': datetime.now().isoformat()
        }],
        documents=[f'Role changed to {new_role}']
    )

    return jsonify({'msg': 'Role updated'}), 200

@admin_bp.route('/admin/logs', methods=['GET'])
@jwt_required()
@role_required('admin')
def view_logs():
    logs = logs_collection.get()
    return jsonify([{
        'user_id': meta.get('user_id'),
        'action': meta.get('action'),
        'timestamp': meta.get('timestamp')
    } for meta in logs['metadatas']])

