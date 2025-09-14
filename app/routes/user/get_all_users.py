from app.orm.controllers.user_controller import UserController
from flask_restx import Resource, fields, reqparse
from app.routes.user import users_ns


user_model = users_ns.model('User', {
    'id': fields.Integer(description='User ID'),
    'username': fields.String(description='Username'),
    'full_name': fields.String(description='Full name'),
    'email': fields.String(description='Email address'),
    'phone': fields.String(description='Phone number'),
    'is_admin': fields.Boolean(description='Admin role'),
    'enable': fields.Boolean(description='User enabled status'),
    'register': fields.String(description='Registration date'),
    'updated_at': fields.String(description='Last update date')
})


@users_ns.route('/all')
class UserListResource(Resource):
    @users_ns.doc('get_all_users')
    @users_ns.param('enabled', 'Filter by enabled status (default: true)', type=bool, default=True)
    @users_ns.param('role', 'Filter by role: admin or user', type=str)
    @users_ns.response(200, 'List of users', model=[user_model])
    def get(self):
        """
        Get all users with optional filtering
        """
        parser = reqparse.RequestParser()
        parser.add_argument('enabled', type=str, default='true', location='args')
        parser.add_argument('role', type=str, location='args')
        args = parser.parse_args()
        
        enabled = args.get('enabled', 'true').lower() in ('true', '1', 'yes', 'on')
        role_filter = args.get('role')

        user_controller = UserController()

        if role_filter:
            if role_filter.lower() == 'admin':
                users = user_controller.get_by_role(True, enabled)
            elif role_filter.lower() == 'user':
                users = user_controller.get_by_role(False, enabled)
            else:
                return {'error': 'Invalid role. Use "admin" or "user"'}, 400
        else:
            users = user_controller.get_all_enable(enabled)

        return [user.model_dump(mode='json') for user in users], 200
