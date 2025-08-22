from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from sqlalchemy import and_, desc
from ..database import db
from .base_controller import BaseController
from .order_detail_controller import OrderDetailController
from ..models.order import Order
from ..models.user import User
from ..schemas.order_schema import (
    OrderCreate, 
    OrderUpdate, 
    OrderRead,
    OrderWithTotals,
    OrderStatus
)

class OrderController(BaseController[Order, OrderCreate, OrderRead, OrderUpdate]):
    def __init__(self):
        super().__init__(Order, OrderCreate, OrderRead, OrderUpdate)
        self.order_detail_controller = OrderDetailController()

    def get_by_user_id(self, user_id: int) -> List[OrderRead]:
        """Get all orders for a specific user"""
        objs = (
            db.session.query(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(desc(self.model.created_at))
            .all()
        )
        return [OrderRead.model_validate(obj) for obj in objs]

    def get_by_status(self, status: str) -> List[OrderRead]:
        """Get all orders with a specific status"""
        objs = (
            db.session.query(self.model)
            .filter(self.model.status == status)
            .order_by(desc(self.model.created_at))
            .all()
        )
        return [OrderRead.model_validate(obj) for obj in objs]

    def get_by_user_and_status(self, user_id: int, status: str) -> List[OrderRead]:
        """Get orders for a specific user with a specific status"""
        objs = (
            db.session.query(self.model)
            .filter(
                and_(
                    self.model.user_id == user_id,
                    self.model.status == status
                )
            )
            .order_by(desc(self.model.created_at))
            .all()
        )
        return [OrderRead.model_validate(obj) for obj in objs]

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[OrderRead]:
        """Get orders within a date range"""
        objs = (
            db.session.query(self.model)
            .filter(
                and_(
                    self.model.created_at >= start_date,
                    self.model.created_at <= end_date
                )
            )
            .order_by(desc(self.model.created_at))
            .all()
        )
        return [OrderRead.model_validate(obj) for obj in objs]