from flask import current_app, send_from_directory
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import NotFound

images_ns = Namespace('image', description='Image operations')

error_model = images_ns.model('Error', {
    'message': fields.String(description='Error message')
})

@images_ns.route('/product/<string:filename>')
@images_ns.param('filename', 'Image filename')
@images_ns.response(404, 'Image not found', error_model)
class ProductImageResource(Resource):
    @images_ns.doc('serve_product_image')
    @images_ns.produces(['image/jpeg', 'image/png'])
    def get(self, filename):
        """
        Serve a product image file
        
        Returns the image file for a product by filename.
        The file must exist in the configured upload folder.
        """
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        current_app.logger.debug(f"Serving image from: {upload_folder}")
        
        try:
            return send_from_directory(upload_folder, filename)
        except FileNotFoundError:
            raise NotFound(f"Image '{filename}' not found")