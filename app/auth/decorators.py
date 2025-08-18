from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

def token_required(f):
    """Custom decorator that combines jwt_required with additional checks"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            if not current_user_id:
                return jsonify({'error': 'Invalid token'}), 401
            return f(current_user_id, *args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 401
    return decorated

def admin_required(f):
    """Decorator for admin-only routes"""
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user_id = get_jwt_identity()
        # Add logic to check if user is admin
        # For now, just pass the user_id
        return f(current_user_id, *args, **kwargs)
    return decorated