
import os
from pathlib import Path
from app.orm.controllers.product_image_controller import ProductImageController
from flask_restx import Resource, fields
from flask import request, current_app
from app.orm.schemas.product_image_schema import ProductImageUpdate
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

product_image_update_model = images_ns.model('ProductImageUpdate', {
    'url': fields.String,
    'alt': fields.String,
    'is_main': fields.Boolean,
    'product_id': fields.Integer
})

@images_ns.route('/<int:image_id>')
@images_ns.param('image_id', 'Image ID')
class ProductImageEditResource(Resource):
    @images_ns.expect(product_image_update_model)
    @images_ns.response(200, 'Image updated', model=product_image_model)
    @images_ns.response(404, 'Image not found')
    def put(self, image_id):
        """
        Update a product image by ID
        """
        data = request.json or {}
        if not data:
            return {'error': 'No data provided'}, 400
        filename = data.get('url')
        if filename:

            upload_folder_rel = current_app.config.get("UPLOAD_FOLDER_REL", "/image/product/")
            ruta_db = os.path.join(upload_folder_rel, filename)
            ruta_db = Path(ruta_db).as_posix()
            data['url'] = ruta_db

        try:
            update_schema = ProductImageUpdate(**data)
        except Exception as e:
            return {'error': str(e)}, 422
        controller = ProductImageController()
        updated = controller.update(image_id, update_schema)
        if not updated:
            return {'error': 'Image not found'}, 404
        return updated.model_dump(mode='json'), 200
    
    @images_ns.response(204, 'Image deleted')
    def delete(self, image_id):
        """
        Delete a product image by ID
        """
        controller = ProductImageController()
        deleted = controller.delete(image_id)
        if not deleted:
            return {'error': 'Image not found'}, 404
        return '', 204