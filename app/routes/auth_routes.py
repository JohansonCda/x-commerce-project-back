from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_services import AuthService
from app.auth.decorators import token_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    """Login endpoint - Simple authentication without database"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    # Simple authentication without database (for testing)
    # In production, you would validate against your user store
    if username == "admin" and password == "admin123":
        user_id = 1
        additional_claims = {"role": "admin", "username": username}
    elif username == "user" and password == "user123":
        user_id = 2
        additional_claims = {"role": "user", "username": username}
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    tokens = AuthService.generate_tokens(user_id, additional_claims)
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user_id,
            'username': username,
            'role': additional_claims['role']
        },
        **tokens
    }), 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Refresh token endpoint"""
    current_user_id = get_jwt_identity()
    # Convert string back to int if needed
    user_id = int(current_user_id) if current_user_id.isdigit() else current_user_id
    new_token = AuthService.create_access_token(user_id)
    
    return jsonify({
        'access_token': new_token,
        'token_type': 'Bearer'
    }), 200

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Logout endpoint"""
    # In a production environment, you might want to blacklist the token
    # For now, we'll just return a success message
    return jsonify({'message': 'Successfully logged out'}), 200

@auth_bp.route("/protected", methods=["GET"])
@token_required
def protected_route(current_user_id):
    """Example protected route"""
    return jsonify({
        'message': f'Hello user {current_user_id}',
        'user_id': current_user_id
    }), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """Get current user information from token"""
    from flask_jwt_extended import get_jwt
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    return jsonify({
        'user_id': current_user_id,
        'username': claims.get('username', 'unknown'),
        'role': claims.get('role', 'user'),
        'message': 'User information retrieved successfully'
    }), 200