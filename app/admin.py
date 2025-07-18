from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .auth import role_required
<<<<<<< HEAD
from chromadb import Client
from .chroma_service import logs_collection
import uuid
from datetime import datetime
import chromadb
from chromadb.config import Settings, DEFAULT_TENANT, DEFAULT_DATABASE

chroma_client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE
)

users_collection = chroma_client.get_or_create_collection(name="users")

=======
from .models import User, Log, db
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_users():
<<<<<<< HEAD
    users = users_collection.get()
    return jsonify([{
        'id': user_id,
        'name': meta.get('name'),
        'email': meta.get('email'),
        'role': meta.get('role')
    } for user_id, meta in zip(users['ids'], users['metadatas'])])
=======
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email, 'role': u.role} for u in users])
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05

@admin_bp.route('/admin/assign-role', methods=['POST'])
@jwt_required()
@role_required('admin')
def assign_role():
    data = request.get_json()
<<<<<<< HEAD
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
=======
    user = User.query.get(data['user_id'])
    user.role = data['new_role']
    db.session.commit()
    log = Log(user_id=user.id, action=f'Role changed to {user.role}')
    db.session.add(log)
    db.session.commit()
    return jsonify({'msg': 'Role updated'})
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05

@admin_bp.route('/admin/logs', methods=['GET'])
@jwt_required()
@role_required('admin')
def view_logs():
<<<<<<< HEAD
    logs = logs_collection.get()
    return jsonify([{
        'user_id': meta.get('user_id'),
        'action': meta.get('action'),
        'timestamp': meta.get('timestamp')
    } for meta in logs['metadatas']])
=======
    logs = Log.query.all()
    return jsonify([{'user_id': l.user_id, 'action': l.action, 'timestamp': l.timestamp} for l in logs])
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05

