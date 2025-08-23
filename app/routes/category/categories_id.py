from app.orm.controllers.category_controller import CategoryController
from flask_restx import Resource, fields
from flask import request
from app.orm.schemas.category_schema import CategoryUpdate
from app.routes.category import categories_ns

category_model = categories_ns.model('Category', {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'enable': fields.Boolean
})

category_update_model = categories_ns.model('CategoryUpdate', {
    'name': fields.String,
    'description': fields.String,
    'enable': fields.Boolean
})

error_model = categories_ns.model('Error', {
    'error': fields.String(description='Error message')
})


@categories_ns.route('/<int:category_id>')
@categories_ns.param('category_id', 'The category ID')
@categories_ns.response(404, 'Category not found', error_model)
class CategoryDetailResource(Resource):
    @categories_ns.response(200, 'Category found', model=category_model)
    def get(self, category_id: int):
        """
        Get a category by ID
        """
        controller = CategoryController()
        category = controller.get_by_id(category_id)
        if not category:
            return {'error': 'Category not found'}, 404
        return category.model_dump(mode='json'), 200

    @categories_ns.expect(category_update_model)
    @categories_ns.response(200, 'Category updated', model=category_model)
    def put(self, category_id: int):
        """
        Update a category by ID
        """
        data = request.json or {}
        if not data:
            return {'error': 'No data provided'}, 400
        try:
            update_schema = CategoryUpdate(**data)
        except Exception as e:
            return {'error': str(e)}, 422
        controller = CategoryController()
        updated = controller.update(category_id, update_schema)
        if not updated:
            return {'error': 'Category not found'}, 404
        return updated.model_dump(mode='json'), 200

    @categories_ns.response(204, 'Category deleted')
    def delete(self, category_id: int):
        """
        Delete (or disable) a category by ID
        """
        controller = CategoryController()
        deleted = controller.delete(category_id)
        if not deleted:
            return {'error': 'Category not found'}, 404
        return {'message': 'Category deleted successfully'}, 204
