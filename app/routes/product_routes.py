
from ..orm.controllers.product_controller import ProductController
from ..orm.controllers.product_image_controller import ProductImageController
import os
from flask import current_app
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import NotFound

# Create namespace for products
products_ns = Namespace('product', description='Product operations')

# Response model (for documentation)
product_category_model = products_ns.model('ProductCategory', {
  'id': fields.Integer,
  'name': fields.String,
  'description': fields.String,
  'enable': fields.Boolean
})

product_model = products_ns.model('Product', {
  'id': fields.Integer,
  'name': fields.String,
  'description': fields.String,
  'price': fields.Float,
  'stock': fields.Integer,
  'enable': fields.Boolean,
  'bought': fields.Integer,
  'registered_at': fields.String,
  'updated_at': fields.String,
  'category_id': fields.Integer,
  'category': fields.Nested(product_category_model)
})

product_with_image_model = products_ns.model('ProductWithImage', {
  'product': fields.Nested(product_model),
  'main_image_url': fields.String,
  'main_image_alt': fields.String
})

error_model = products_ns.model('Error', {
  'error': fields.String(description='Error message')
})

@products_ns.route('/<int:product_id>')
@products_ns.param('product_id', 'The product ID')
@products_ns.response(404, 'Product not found', error_model)
class ProductResource(Resource):
  @products_ns.doc('get_product_with_image')
  @products_ns.marshal_with(product_with_image_model)
  def get(self, product_id):
    """
    Get product and its main image
    Returns the product data and the main image URL (if any) for the given product ID.
    """
    product_controller = ProductController()
    image_controller = ProductImageController()
    PRODUCT_IMAGE_URL = "/api/image/product/"

    product = product_controller.get_by_id(product_id)
    if not product:
      return {"error": "Product not found"}, 404

    main_image = image_controller.get_main_image(product_id)
    if main_image:
      host = current_app.config.get('HOST_URL', 'http://localhost:5000')
      image_url = f"{host}{PRODUCT_IMAGE_URL}{os.path.basename(main_image.url)}"
    else:
      image_url = None

    return {
      "product": product.model_dump(),
      "main_image_url": image_url,
      "main_image_alt": main_image.alt if main_image else None
    }
