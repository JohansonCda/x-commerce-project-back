from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask import current_app

def configure_jwt(app):
    """Configure JWT settings"""
    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY', 'super-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['JWT_ALGORITHM'] = 'HS256'
    
    jwt = JWTManager(app)
    
    # Import handlers to register callbacks
    from .handlers import register_jwt_handlers
    register_jwt_handlers(jwt)
    
    return jwt