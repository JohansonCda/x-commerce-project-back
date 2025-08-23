from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import NotFound

# Create namespace for main
main_ns = Namespace('main', description='Main operations')

# Response model (optional, for documentation)
error_model = main_ns.model('Error', {
    'message': fields.String(description='Error message')
})

@main_ns.route("", methods=["GET"])
@main_ns.response(404, 'Page not found', error_model)
class IndexResource(Resource):
    def get(self):
        return {"message": "API corriendo..."}