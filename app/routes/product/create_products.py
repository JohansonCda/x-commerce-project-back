from app.orm.controllers.product_controller import ProductController
from flask_restx import Resource, fields
from flask import request
from app.orm.schemas.product_schema import ProductCreate
from app.routes.product import products_ns

product_model = products_ns.models.get('Product')
product_create_model = products_ns.model('ProductCreate', {
  'name': fields.String(required=True),
  'description': fields.String,
  'price': fields.Float(required=True),
  'stock': fields.Integer(required=True),
  'bought': fields.Integer,
  'enable': fields.Boolean,
  'category_id': fields.Integer(required=True)
})

@products_ns.route('/')
class ProductCreateResource(Resource):
  @products_ns.expect(product_create_model)
  @products_ns.response(201, 'Product created', model=product_model)
  def post(self):
    """
    Create a new product
    """
    data = request.json or {}
    if not data:
      return {'error': 'No data provided'}, 400

    try:
      create_schema = ProductCreate(**data)
    except Exception as e:
      return {'error': str(e)}, 422

    controller = ProductController()
    created = controller.create(create_schema)
    return created.model_dump(mode='json'), 201
