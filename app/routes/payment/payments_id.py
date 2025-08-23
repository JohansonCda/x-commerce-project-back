from app.orm.controllers.payment_controller import PaymentController
from flask_restx import Resource, fields
from flask import request
from app.orm.schemas.payment_schema import PaymentUpdate
from app.routes.payment import payments_ns

payment_model = payments_ns.model('Payment', {
    'id': fields.Integer,
    'order_id': fields.Integer,
    'mount': fields.Float,
    'pay_method': fields.String,
    'status_id': fields.Integer,
    'registered_at': fields.String,
    'updated_at': fields.String
})

payment_update_model = payments_ns.model('PaymentUpdate', {
    'order_id': fields.Integer,
    'mount': fields.Float,
    'pay_method': fields.String,
    'status_id': fields.Integer
})

error_model = payments_ns.model('Error', {
    'error': fields.String(description='Error message')
})

@payments_ns.route('/<int:payment_id>')
@payments_ns.param('payment_id', 'The payment ID')
@payments_ns.response(404, 'Payment not found', error_model)
class PaymentDetailResource(Resource):
    @payments_ns.response(200, 'Payment found', model=payment_model)
    def get(self, payment_id: int):
        """
        Get a payment by ID
        """
        controller = PaymentController()
        payment = controller.get_by_id(payment_id)
        if not payment:
            return {'error': 'Payment not found'}, 404
        return payment.model_dump(mode='json'), 200

    @payments_ns.expect(payment_update_model)
    @payments_ns.response(200, 'Payment updated', model=payment_model)
    def put(self, payment_id: int):
        """
        Update a payment by ID
        """
        data = request.json or {}
        if not data:
            return {'error': 'No data provided'}, 400
        try:
            update_schema = PaymentUpdate(**data)
        except Exception as e:
            return {'error': str(e)}, 422
        controller = PaymentController()
        updated = controller.update(payment_id, update_schema)
        if not updated:
            return {'error': 'Payment not found'}, 404
        return updated.model_dump(mode='json'), 200

    @payments_ns.response(204, 'Payment deleted')
    def delete(self, payment_id: int):
        """
        Delete (or disable) a payment by ID
        """
        controller = PaymentController()
        deleted = controller.delete(payment_id)
        if not deleted:
            return {'error': 'Payment not found'}, 404
        return {'message': 'Payment deleted successfully'}, 204
