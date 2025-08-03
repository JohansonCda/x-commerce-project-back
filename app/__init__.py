from flask import Flask
from .orm.database.base import db
from flask_jwt_extended import JWTManager
from app.routes.main_routes import main_bp
from app.config.config import Config
from .orm.models import *

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # Registrar rutas
    app.register_blueprint(main_bp)

    return app
