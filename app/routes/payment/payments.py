from app.orm.controllers.payment_controller import PaymentController
from flask_restx import Resource, fields
from flask import request
from app.orm.schemas.payment_schema import PaymentCreate
from app.routes.payment import payments_ns
from typing import List
from pydantic import BaseModel

class PaymentListResponse(BaseModel):
    payments: List[PaymentCreate]

payment_model = payments_ns.model('Payment', {
    'id': fields.Integer,
    'order_id': fields.Integer,
    'mount': fields.Float,
    'pay_method': fields.String,
    'status_id': fields.Integer,
    'registered_at': fields.String,
    'updated_at': fields.String
})

payment_create_model = payments_ns.model('PaymentCreate', {
    'order_id': fields.Integer(required=True),
    'mount': fields.Float(required=True),
    'pay_method': fields.String(required=True),
    'status_id': fields.Integer(required=True)
})

error_model = payments_ns.model('Error', {
    'error': fields.String(description='Error message')
})

@payments_ns.route('/')
class PaymentListResource(Resource):
    @payments_ns.response(200, 'List of payments', model=[payment_model])
    def get(self):
        """
        List all payments
        """
        controller = PaymentController()
        payments = controller.get_all()
        return [p.model_dump(mode='json') for p in payments], 200

    @payments_ns.expect(payment_create_model)
    @payments_ns.response(201, 'Payment created', model=payment_model)
    def post(self):
        """
        Create a new payment
        """
        data = request.json or {}
        if not data:
            return {'error': 'No data provided'}, 400
        try:
            create_schema = PaymentCreate(**data)
        except Exception as e:
            return {'error': str(e)}, 422
        controller = PaymentController()
        created = controller.create(create_schema)
        return created.model_dump(mode='json'), 201
