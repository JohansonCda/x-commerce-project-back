from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.token_controller import TokenController

token_bp = Blueprint("token", __name__, url_prefix="/api/token")

@token_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    """
    Refresh access token using refresh token
    
    Requires:
        - Valid refresh token in Authorization header
        
    Returns:
        - New access token with updated claims
        - User information
        - Token metadata
    """
    response_data, status_code = TokenController.refresh_access_token()
    return jsonify(response_data), status_code

@token_bp.route("/validate", methods=["GET"])
@jwt_required()
def validate_token():
    """
    Validate current access token and return token information
    
    Requires:
        - Valid access token in Authorization header
        
    Returns:
        - Token validity status
        - Token metadata (expiry, user info, etc.)
    """
    response_data, status_code = TokenController.validate_token()
    return jsonify(response_data), status_code

@token_bp.route("/revoke", methods=["POST"])
@jwt_required()
def revoke_token():
    """
    Revoke/blacklist current token (logout)
    
    Requires:
        - Valid access token in Authorization header
        
    Returns:
        - Confirmation of token revocation
        - Token metadata
    """
    response_data, status_code = TokenController.revoke_token()
    return jsonify(response_data), status_code

@token_bp.route("/info", methods=["GET"])
@jwt_required()
def get_token_info():
    """
    Get detailed information about the current token
    Alias for /validate endpoint
    """
    response_data, status_code = TokenController.validate_token()
    return jsonify(response_data), status_code
