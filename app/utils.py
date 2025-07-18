from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from .models import User

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user = User.query.get(get_jwt_identity())
            if user.role != role:
                return jsonify({'msg': 'Unauthorized'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
