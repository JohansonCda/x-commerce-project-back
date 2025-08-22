from flask import Flask
from .orm.database.base import db
#from flask_jwt_extended import JWTManager
from app.config.config import Config
from .auth.jwt_config import configure_jwt 
from app.routes.auth_routes import auth_bp
from app.routes.main_routes import main_bp
from .orm.models import *

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)

    # Configure JWT
    configure_jwt(app)

    # Register routes
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app
