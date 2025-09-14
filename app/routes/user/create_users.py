from app.orm.controllers.user_controller import UserController
from flask_restx import Resource, fields
from flask import request
from app.orm.schemas.user_schema import UserCreate
from app.routes.user import users_ns

user_model = users_ns.models.get('User')
user_create_model = users_ns.model('UserCreate', {
    'username': fields.String(required=True, description='Username'),
    'full_name': fields.String(required=True, description='Full name of the user'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='User password (min 6 characters)'),
    'phone': fields.String(required=True, description='Phone number (max 15 characters)'),
    'is_admin': fields.Boolean(default=False, description='Whether the user is an admin'),
    'enable': fields.Boolean(default=True, description='Whether the user is enabled')
})

error_model = users_ns.model('Error', {
    'error': fields.String(description='Error message')
})

@users_ns.route('/')
class UserCreateResource(Resource):
    @users_ns.expect(user_create_model)
    @users_ns.response(201, 'User created', model=user_model)
    @users_ns.response(400, 'Invalid data or validation error', model=error_model)
    @users_ns.response(422, 'Schema validation error', model=error_model)
    @users_ns.response(500, 'Internal server error', model=error_model)
    def post(self):
        """
        Create a new user
        """
        data = request.json or {}
        if not data:
            return {'error': 'No data provided'}, 400

        try:
            create_schema = UserCreate(**data)
        except Exception as e:
            return {'error': str(e)}, 422

        controller = UserController()
        
        try:
            created = controller.create(create_schema)
            return created.model_dump(mode='json'), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'An error occurred while creating the user: {str(e)}'}, 500
