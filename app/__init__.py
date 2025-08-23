from flask import Flask
from flask_restx import Api, Resource, fields
from .orm.database.base import db
#from flask_jwt_extended import JWTManager
from app.config.config import Config
from .auth.jwt_config import configure_jwt 
from app.routes.auth_routes import auth_ns
from app.routes.main_routes import main_ns
from app.routes.image_routes import images_ns
from app.routes.product_routes import products_ns
from .orm.models import *

def create_app():
    app = Flask(__name__)

    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Type in the value input box: **Bearer {your_token}**'
        }
    }

    api = Api(
        app,
        version='1.0',
        title='X-Commerce API',
        description='Documentación de la API de X-Commerce',
        doc='/docs/',
        prefix='/api',
        authorizations=authorizations,
        security='Bearer Auth'
    )



    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)

    # Configure JWT
    configure_jwt(app)

    # Register routes
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(products_ns, path='/product')
    api.add_namespace(images_ns, path='/image')
    api.add_namespace(main_ns, path='/')

    return app
