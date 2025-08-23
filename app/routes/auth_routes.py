from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.auth_services import AuthService
from app.auth.decorators import token_required

auth_ns = Namespace('auth', description='Authentication operations')

# Models for documentation
user_model = auth_ns.model('User', {
    'id': fields.Integer,
    'username': fields.String,
    'role': fields.String
})

login_request_model = auth_ns.model('LoginRequest', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

login_response_model = auth_ns.model('LoginResponse', {
    'message': fields.String,
    'user': fields.Nested(user_model),
    'access_token': fields.String,
    'refresh_token': fields.String,
    'token_type': fields.String
})

error_model = auth_ns.model('AuthError', {
    'error': fields.String(description='Error message')
})

@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.expect(login_request_model)
    @auth_ns.response(200, 'Login successful', login_response_model)
    @auth_ns.response(400, 'Bad request', error_model)
    @auth_ns.response(401, 'Invalid credentials', error_model)
    def post(self):
        """Login endpoint - Simple authentication without database"""
        data = request.get_json()
        if not data:
            return {'error': 'No data provided'}, 400
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return {'error': 'Username and password required'}, 400
        if username == "admin" and password == "admin123":
            user_id = 1
            additional_claims = {"role": "admin", "username": username}
        elif username == "user" and password == "user123":
            user_id = 2
            additional_claims = {"role": "user", "username": username}
        else:
            return {'error': 'Invalid credentials'}, 401
        tokens = AuthService.generate_tokens(user_id, additional_claims)
        return {
            'message': 'Login successful',
            'user': {
                'id': user_id,
                'username': username,
                'role': additional_claims['role']
            },
            **tokens,
            'token_type': 'Bearer'
        }, 200

@auth_ns.route('/refresh')
class RefreshResource(Resource):
    @auth_ns.doc(security='Bearer Auth')
    @auth_ns.response(200, 'Token refreshed', model=auth_ns.model('RefreshResponse', {
        'access_token': fields.String,
        'token_type': fields.String
    }))
    @jwt_required(refresh=True)
    def post(self):
        """Refresh token endpoint"""
        current_user_id = get_jwt_identity()
        user_id = int(current_user_id) if str(current_user_id).isdigit() else current_user_id
        new_token = AuthService.create_access_token(user_id)
        return {
            'access_token': new_token,
            'token_type': 'Bearer'
        }, 200

@auth_ns.route('/logout')
class LogoutResource(Resource):
    @auth_ns.doc(security='Bearer Auth')
    @auth_ns.response(200, 'Successfully logged out', model=auth_ns.model('LogoutResponse', {
        'message': fields.String
    }))
    @auth_ns.response(401, 'Invalid token', error_model)
    @jwt_required()
    def post(self):
        """Logout endpoint - Requires valid JWT token"""
        return {'message': 'Successfully logged out'}, 200

@auth_ns.route('/me')
class MeResource(Resource):
    @auth_ns.doc(security='Bearer Auth')
    @auth_ns.response(200, 'User info', model=auth_ns.model('MeResponse', {
        'user_id': fields.String,
        'username': fields.String,
        'role': fields.String,
        'message': fields.String
    }))
    @auth_ns.response(401, 'Invalid token', error_model)
    @jwt_required()
    def get(self):
        """Get current user information from token - Requires valid JWT token"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        return {
            'user_id': current_user_id,
            'username': claims.get('username', 'unknown'),
            'role': claims.get('role', 'user'),
            'message': 'User information retrieved successfully'
        }, 200