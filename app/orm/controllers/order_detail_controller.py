from typing import List, Optional
from decimal import Decimal
from sqlalchemy import and_
from ..database import db
from .base_controller import BaseController
from ..models.order_detail import OrderDetail
from ..models.order import Order
from ..models.product import Product
from ..schemas.order_detail_schema import (
    OrderDetailCreate, 
    OrderDetailUpdate, 
    OrderDetailRead,
    OrderDetailWithTotals
)

class OrderDetailController(BaseController[OrderDetail, OrderDetailCreate, OrderDetailRead, OrderDetailUpdate]):
    def __init__(self):
        super().__init__(OrderDetail, OrderDetailCreate, OrderDetailRead, OrderDetailUpdate)

    def get_by_order_id(self, order_id: int) -> List[OrderDetailRead]:
        """Get all order details for a specific order"""
        objs = (
            db.session.query(self.model)
            .filter(self.model.order_id == order_id)
            .all()
        )
        return [OrderDetailRead.model_validate(obj) for obj in objs]

    def get_by_product_id(self, product_id: int) -> List[OrderDetailRead]:
        """Get all order details for a specific product"""
        objs = (
            db.session.query(self.model)
            .filter(self.model.product_id == product_id)
            .all()
        )
        return [OrderDetailRead.model_validate(obj) for obj in objs]

    def get_by_order_and_product(self, order_id: int, product_id: int) -> Optional[OrderDetailRead]:
        """Get specific order detail by order and product"""
        obj = (
            db.session.query(self.model)
            .filter(
                and_(
                    self.model.order_id == order_id,
                    self.model.product_id == product_id
                )
            )
            .first()
        )
        return OrderDetailRead.model_validate(obj) if obj else None

    def get_with_totals(self, order_detail_id: int) -> Optional[OrderDetailWithTotals]:
        """Get order detail with calculated totals"""
        order_detail = self.get_by_id(order_detail_id)
        if not order_detail:
            return None
        return OrderDetailWithTotals.from_order_detail(order_detail)

    def get_order_totals(self, order_id: int) -> dict:
        """Calculate totals for an entire order"""
        order_details = self.get_by_order_id(order_id)
        
        total_items = sum(detail.quantity for detail in order_details)
        total_amount = sum(
            detail.quantity * detail.unit_price for detail in order_details
        )
        
        return {
            "order_id": order_id,
            "total_items": total_items,
            "total_amount": total_amount,
            "details_count": len(order_details)
        }

    def get_by_price_range(self, min_price: Decimal, max_price: Decimal) -> List[OrderDetailRead]:
        """Get order details within a unit price range"""
        objs = (
            db.session.query(self.model)
            .filter(
                and_(
                    self.model.unit_price >= min_price,
                    self.model.unit_price <= max_price
                )
            )
            .all()
        )
        return [OrderDetailRead.model_validate(obj) for obj in objs]

    def get_by_quantity_range(self, min_quantity: int, max_quantity: int) -> List[OrderDetailRead]:
        """Get order details within a quantity range"""
        objs = (
            db.session.query(self.model)
            .filter(
                and_(
                    self.model.quantity >= min_quantity,
                    self.model.quantity <= max_quantity
                )
            )
            .all()
        )
        return [OrderDetailRead.model_validate(obj) for obj in objs]

    def update_quantity(self, order_detail_id: int, new_quantity: int) -> Optional[OrderDetailRead]:
        """Update only the quantity of an order detail"""
        if new_quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
            
        return self.update(order_detail_id, {"quantity": new_quantity})

    def update_unit_price(self, order_detail_id: int, new_price: Decimal) -> Optional[OrderDetailRead]:
        """Update only the unit price of an order detail"""
        if new_price < 0:
            raise ValueError("Unit price cannot be negative")
            
        return self.update(order_detail_id, {"unit_price": new_price})