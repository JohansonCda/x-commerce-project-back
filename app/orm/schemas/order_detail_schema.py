from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class OrderDetailBase(BaseModel):
    """Base fields for order details"""
    order_id: int = Field(..., gt=0, description="Order ID")
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, description="Product quantity")
    unit_price: Decimal = Field(..., ge=0, description="Unit price at time of order")

class OrderDetailCreate(BaseModel):
    """Schema for creating new order details"""
    order_id: int = Field(..., gt=0, description="Order ID")
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, description="Product quantity")
    unit_price: Decimal = Field(..., ge=0, description="Unit price at time of order")

class OrderDetailUpdate(BaseModel):
    """Schema for updating order details"""
    order_id: Optional[int] = Field(None, gt=0, description="Order ID")
    product_id: Optional[int] = Field(None, gt=0, description="Product ID")
    quantity: Optional[int] = Field(None, gt=0, description="Product quantity")
    unit_price: Optional[Decimal] = Field(None, ge=0, description="Unit price at time of order")

class OrderDetailRead(OrderDetailBase):
    """Complete order detail schema including read-only fields"""
    id: int
    model_config = ConfigDict(from_attributes=True)

class OrderDetailWithTotals(OrderDetailRead):
    """Order detail with calculated totals"""
    total_price: Decimal = Field(..., description="Total price (quantity * unit_price)")
    
    @classmethod
    def from_order_detail(cls, order_detail: OrderDetailRead) -> "OrderDetailWithTotals":
        """Create OrderDetailWithTotals from OrderDetailRead"""
        total_price = order_detail.quantity * order_detail.unit_price
        return cls(
            **order_detail.model_dump(),
            total_price=total_price
        )