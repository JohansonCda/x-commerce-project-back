from app.orm.controllers.product_controller import ProductController
from app.orm.controllers.product_image_controller import ProductImageController
from flask_restx import Resource, fields, reqparse
from app.orm.schemas.product_schema import ProductRead
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


@products_ns.route('/all')
class ProductListResource(Resource):
	@products_ns.doc('get_all_products')
	@products_ns.param('with_images', 'Include images for each product (default: true)', type=bool, default=True)
	def get(self):
		"""
		Get all products, optionally including images
		"""
		parser = reqparse.RequestParser()
		parser.add_argument('with_images', type=str, default='true', location='args')
		args = parser.parse_args()
		with_images = args.get('with_images', 'true').lower() in ('true', '1', 'yes', 'on')

		product_controller = ProductController()
		image_controller = ProductImageController()

		products = product_controller.get_all_enable()

		if with_images:
			result = []
			for product in products:
				images = image_controller.get_by_product(product.id)
				response = ProductWithImagesResponse(
					product=product,
					images=images
				)
				result.append(response.model_dump(mode='json'))
			return result, 200
		else:
			return [product.model_dump(mode='json') for product in products], 200
