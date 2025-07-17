from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .auth import role_required
from .models import User, Log, db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email, 'role': u.role} for u in users])

@admin_bp.route('/admin/assign-role', methods=['POST'])
@jwt_required()
@role_required('admin')
def assign_role():
    data = request.get_json()
    user = User.query.get(data['user_id'])
    user.role = data['new_role']
    db.session.commit()
    log = Log(user_id=user.id, action=f'Role changed to {user.role}')
    db.session.add(log)
    db.session.commit()
    return jsonify({'msg': 'Role updated'})

@admin_bp.route('/admin/logs', methods=['GET'])
@jwt_required()
@role_required('admin')
def view_logs():
    logs = Log.query.all()
    return jsonify([{'user_id': l.user_id, 'action': l.action, 'timestamp': l.timestamp} for l in logs])

