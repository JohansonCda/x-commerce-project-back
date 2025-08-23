from app.orm.controllers.product_controller import ProductController
from app.orm.controllers.product_image_controller import ProductImageController
from flask_restx import Resource, fields
from flask import request
from app.orm.schemas.product_schema import ProductRead, ProductUpdate
from app.orm.schemas.product_image_schema import ProductImageRead
from typing import Optional, List
from pydantic import BaseModel
from app.routes.product import products_ns


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


product_update_model = products_ns.model('ProductUpdate', {
  'name': fields.String,
  'description': fields.String,
  'price': fields.Float,
  'stock': fields.Integer,
  'bought': fields.Integer,
  'enable': fields.Boolean,
  'category_id': fields.Integer
})

@products_ns.route('/<int:product_id>')
@products_ns.param('product_id', 'The product ID')
@products_ns.response(404, 'Product not found', error_model)
class ProductDetailResource(Resource):
  @products_ns.doc('get_product_with_images')
  @products_ns.response(200, 'List of products', model=product_model)
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

  @products_ns.expect(product_update_model)
  @products_ns.response(200, 'Product updated', model=product_model)
  def put(self, product_id):
    """
    Update a product by ID
    """
    data = request.json or {}
    if not data:
      return {'error': 'No data provided'}, 400

    try:
      update_schema = ProductUpdate(**data)
    except Exception as e:
      return {'error': str(e)}, 422

    controller = ProductController()
    updated = controller.update(product_id, update_schema)
    if not updated:
      return {'error': 'Product not found'}, 404
    return updated.model_dump(mode='json'), 200
  
  @products_ns.response(204, 'Product deleted')
  def delete(self, product_id):
    """
    Delete (or disable) a product by ID
    """
    controller = ProductController()
    deleted = controller.delete(product_id)
    if not deleted:
      return {'error': 'Product not found'}, 404
    return {'message': 'Product deleted successfully'}, 204
