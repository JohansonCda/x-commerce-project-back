from app.orm.controllers.user_controller import UserController
from flask_restx import Resource, fields
from flask import request
from app.orm.schemas.user_schema import UserUpdate
from app.routes.user import users_ns
import re


user_model = users_ns.model('User', {
    'id': fields.Integer(description='User ID'),
    'username': fields.String(description='Username'),
    'full_name': fields.String(description='Full name'),
    'email': fields.String(description='Email address'),
    'phone': fields.String(description='Phone number'),
    'is_admin': fields.Boolean(description='Admin role'),
    'enable': fields.Boolean(description='User enabled status'),
    'register': fields.String(description='Registration date'),
    'updated': fields.String(description='Last update date')
})

user_update_model = users_ns.model('UserUpdate', {
    'username': fields.String(required=False, description='Username'),
    'full_name': fields.String(required=False, description='Full name of the user'),
    'email': fields.String(required=False, description='Email address'),
    'password': fields.String(required=False, description='User password (min 6 characters)'),
    'phone': fields.String(required=False, description='Phone number (max 15 characters)'),
    'is_admin': fields.Boolean(required=False, description='Whether the user is an admin'),
    'enable': fields.Boolean(required=False, description='Whether the user is enabled')
})

error_model = users_ns.model('Error', {
    'error': fields.String(description='Error message')
})


@users_ns.route('/<int:user_id>')
@users_ns.param('user_id', 'The user ID')
@users_ns.response(404, 'User not found', error_model)
class UserDetailResource(Resource):
    @users_ns.doc('get_user_by_id')
    @users_ns.response(200, 'User found', model=user_model)
    def get(self, user_id: int):
        """
        Get user by ID
        Returns the user data for the given user ID.
        """
        user_controller = UserController()
        user = user_controller.get_by_id(user_id)
        
        if not user:
            return {"error": "User not found"}, 404

        return user.model_dump(mode='json')

    @users_ns.expect(user_update_model)
    @users_ns.response(200, 'User updated', model=user_model)
    @users_ns.response(400, 'Invalid data or validation error', model=error_model)
    @users_ns.response(404, 'User not found', model=error_model)
    @users_ns.response(422, 'Schema validation error', model=error_model)
    @users_ns.response(500, 'Internal server error', model=error_model)
    def put(self, user_id: int):
        """
        Update a user by ID
        """
        data = request.json or {}
        if not data:
            return {'error': 'No data provided'}, 400

        try:
            update_schema = UserUpdate(**data)
        except Exception as e:
            return {'error': str(e)}, 422

        controller = UserController()
        
        if 'email' in data:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, data['email']):
                return {'error': 'Invalid email format'}, 400
            
            existing_users = controller.get_by_email(data['email'])
            existing_users = [u for u in existing_users if u.id != user_id]
            if existing_users:
                return {'error': 'Email already exists'}, 400

        if 'username' in data:
            existing_users = controller.get_by_username(data['username'])
            existing_users = [u for u in existing_users if u.id != user_id]
            if existing_users:
                return {'error': 'Username already exists'}, 400

        try:
            updated = controller.update(user_id, update_schema)
            if not updated:
                return {'error': 'User not found'}, 404
            return updated.model_dump(mode='json'), 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'An error occurred while updating the user: {str(e)}'}, 500
    
    @users_ns.response(204, 'User deleted')
    @users_ns.response(404, 'User not found', model=error_model)
    def delete(self, user_id: int):
        """
        Delete (or disable) a user by ID
        """
        controller = UserController()
        deleted = controller.delete(user_id)
        if not deleted:
            return {'error': 'User not found'}, 404
        return {'message': 'User deleted successfully'}, 204
