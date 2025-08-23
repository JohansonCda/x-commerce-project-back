import os
from flask_restx import Resource, fields
from flask import request
from app.orm.controllers.product_image_controller import ProductImageController
from app.routes.image import images_ns

product_image_model = images_ns.model('ProductImage', {
    'id': fields.Integer,
    'url': fields.String,
    'alt': fields.String,
    'is_main': fields.Boolean,
    'product_id': fields.Integer,
    'registered_at': fields.String,
    'updated_at': fields.String
})

product_image_create_model = images_ns.model('ProductImageCreate', {
    'url': fields.String(required=True),
    'alt': fields.String,
    'is_main': fields.Boolean,
    'product_id': fields.Integer(required=True)
})

@images_ns.route('/')
class ProductImageCreateResource(Resource):
    @images_ns.expect(product_image_create_model)
    @images_ns.response(201, 'Image registered', model=product_image_model)
    def post(self):
        """
        Register a new image for a product
        """
        data = request.json or {}
        if not data:
            return {'error': 'No data provided'}, 400

        filename = data.get('url')
        product_id = data.get('product_id')
        is_main = data.get('is_main', False)
        alt = data.get('alt')
        if not filename or not product_id:
            return {'error': 'Filename (url) and product_id are required'}, 400

        controller = ProductImageController()
        try:
            created = controller.register_image(
                product_id=product_id,
                filename=filename,
                is_main=is_main,
                alt=alt
            )
        except Exception as e:
            return {'error': str(e)}, 422
        return created.model_dump(mode='json'), 201
