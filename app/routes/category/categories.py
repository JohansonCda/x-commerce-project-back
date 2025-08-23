from app.orm.controllers.category_controller import CategoryController
from flask_restx import Resource, fields
from flask import request
from app.orm.schemas.category_schema import CategoryCreate, CategoryRead
from app.routes.category import categories_ns
from typing import List
from pydantic import BaseModel


class CategoryListResponse(BaseModel):
    categories: List[CategoryRead]

category_model = categories_ns.model('Category', {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'enable': fields.Boolean
})

category_create_model = categories_ns.model('CategoryCreate', {
    'name': fields.String(required=True),
    'description': fields.String,
    'enable': fields.Boolean
})

error_model = categories_ns.model('Error', {
    'error': fields.String(description='Error message')
})

@categories_ns.route('/')
class CategoryListResource(Resource):
    @categories_ns.response(200, 'List of categories', model=[category_model])
    def get(self):
        """
        List all categories
        """
        controller = CategoryController()
        categories = controller.get_all_enable()
        return [c.model_dump(mode='json') for c in categories], 200

    @categories_ns.expect(category_create_model)
    @categories_ns.response(201, 'Category created', model=category_model)
    def post(self):
        """
        Create a new category
        """
        data = request.json or {}
        if not data:
            return {'error': 'No data provided'}, 400
        try:
            create_schema = CategoryCreate(**data)
        except Exception as e:
            return {'error': str(e)}, 422
        controller = CategoryController()
        created = controller.create(create_schema)
        return created.model_dump(mode='json'), 201