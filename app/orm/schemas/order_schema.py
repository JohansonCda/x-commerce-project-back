from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from .order_detail_schema import OrderDetailRead, OrderDetailCreate

class OrderBase(BaseModel):
    """Base fields for orders"""
    user_id: int = Field(..., gt=0, description="User ID who placed the order")
    status: str = Field(default="pending", max_length=50, description="Order status")

class OrderCreate(BaseModel):
    """Schema for creating new orders"""
    user_id: int = Field(..., gt=0, description="User ID who placed the order")
    status: str = Field(default="pending", max_length=50, description="Order status")
    details: Optional[List[OrderDetailCreate]] = Field(default=[], description="Order details")

class OrderUpdate(BaseModel):
    """Schema for updating orders"""
    user_id: Optional[int] = Field(None, gt=0, description="User ID who placed the order")
    status: Optional[str] = Field(None, max_length=50, description="Order status")

class OrderRead(OrderBase):
    """Complete order schema including read-only fields"""
    id: int
    created_at: datetime = Field(..., description="Order creation timestamp")
    
    details: Optional[List[OrderDetailRead]] = Field(default=[], description="Order details")
 
    model_config = ConfigDict(from_attributes=True)

class OrderWithTotals(OrderRead):
    """Order with calculated totals and summary"""
    total_items: int = Field(..., description="Total number of items in order")
    total_amount: Decimal = Field(..., description="Total order amount")
    
    @classmethod
    def from_order(cls, order: OrderRead) -> "OrderWithTotals":
        """Create OrderWithTotals from OrderRead"""
        total_items = sum(detail.quantity for detail in order.details) if order.details else 0
        total_amount = sum(
            detail.quantity * detail.unit_price for detail in order.details
        ) if order.details else Decimal('0.00')
        
        return cls(
            **order.model_dump(),
            total_items=total_items,
            total_amount=total_amount
        )

# Status enums for validation
class OrderStatus:
    """Order status constants"""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    
    @classmethod
    def all_statuses(cls) -> List[str]:
        """Get all available order statuses"""
        return [cls.PENDING, cls.PROCESSING, cls.SHIPPED, cls.DELIVERED, cls.CANCELLED]

class OrderStatusUpdate(BaseModel):
    """Schema for updating only order status"""
    status: str = Field(..., description="New order status")
    
    def validate_status(self) -> bool:
        """Validate if status is allowed"""
        return self.status in OrderStatus.all_statuses()