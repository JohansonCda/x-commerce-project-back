from typing import List
from ..database import db
from .base_controller import BaseController
from ..models.payment import Payment
from ..schemas.payment_schema import PaymentCreate, PaymentRead, PaymentUpdate

class PaymentController(BaseController[Payment, PaymentCreate, PaymentRead, PaymentUpdate]):
    def __init__(self):
        super().__init__(Payment, PaymentCreate, PaymentRead, PaymentUpdate)

    def get_by_order(self, order_id: int) -> List[PaymentRead]:
        """Get all payments for an order"""
        objs = (
            db.session.query(self.model)
            .filter(self.model.order_id == order_id)
            .all()
        )
        return [PaymentRead.model_validate(obj) for obj in objs]

    def get_by_status(self, status_id: int) -> List[PaymentRead]:
        """Get all payments with a specific status"""
        objs = (
            db.session.query(self.model)
            .filter(self.model.status_id == status_id)
            .all()
        )
        return [PaymentRead.model_validate(obj) for obj in objs]
    
    def get_by_amount(self, min_amount: float = None, max_amount: float = None) -> List[PaymentRead]:
        """Get all payments with amount greater than or less than a value"""
        query = db.session.query(self.model)
        if min_amount is not None:
            query = query.filter(self.model.mount >= min_amount)
        if max_amount is not None:
            query = query.filter(self.model.mount <= max_amount)
        objs = query.all()
        return [PaymentRead.model_validate(obj) for obj in objs]

    def get_by_pay_method(self, pay_method: str) -> List[PaymentRead]:
        """Get all payments by payment method"""
        objs = (
            db.session.query(self.model)
            .filter(self.model.pay_method == pay_method)
            .all()
        )
        return [PaymentRead.model_validate(obj) for obj in objs]

    def _validate_create(self, obj_in: PaymentCreate):
        pass
