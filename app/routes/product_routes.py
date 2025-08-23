

from app.orm.controllers.product_controller import ProductController
from app.orm.controllers.product_image_controller import ProductImageController
from flask_restx import Namespace, Resource, fields
from app.orm.schemas.product_schema import ProductRead
from app.orm.schemas.product_image_schema import ProductImageRead
from typing import Optional, List
from pydantic import BaseModel


products_ns = Namespace('product', description='Product operations')

class ProductWithImagesResponse(BaseModel):
  product: ProductRead
  images: Optional[List[ProductImageRead]]


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


product_image_model = products_ns.model('ProductImage', {
  'id': fields.Integer,
  'url': fields.String,
  'alt': fields.String,
  'is_main': fields.Boolean,
  'product_id': fields.Integer,
  'registered_at': fields.String,
  'updated_at': fields.String
})

product_with_images_model = products_ns.model('ProductWithImages', {
  'product': fields.Nested(product_model),
  'images': fields.List(fields.Nested(product_image_model))
})

error_model = products_ns.model('Error', {
  'error': fields.String(description='Error message')
})


@products_ns.route('/<int:product_id>')
@products_ns.param('product_id', 'The product ID')
@products_ns.response(404, 'Product not found', error_model)
class ProductResource(Resource):
  @products_ns.doc('get_product_with_images')
  @products_ns.marshal_with(product_with_images_model)
  def get(self, product_id: int):
    """
    Get product and all its images
    Returns the product data and all associated images for the given product ID.
    """
    product_controller = ProductController()
    image_controller = ProductImageController()

    product = product_controller.get_by_id(product_id)
    if not product:
      return {"error": "Product not found"}, 404

    images = image_controller.get_by_product(product_id)

    response = ProductWithImagesResponse(
      product=product,
      images=images
    )
    return response.dict()
