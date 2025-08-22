from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from .status_schema import StatusRead

class PayBase(BaseModel):
    order_id: int = Field(..., gt=0, description="Order ID")
    mount: float = Field(..., ge=0, description="Payment amount")
    pay_method: str = Field(..., max_length=50, description="Payment method")
    status_id: int = Field(..., gt=0, description="Status ID")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

class PayCreate(BaseModel):
    order_id: int = Field(..., gt=0)
    mount: float = Field(..., ge=0)
    pay_method: str = Field(..., max_length=50)
    status_id: int = Field(..., gt=0)

class PayUpdate(BaseModel):
    order_id: Optional[int] = Field(None, gt=0)
    mount: Optional[float] = Field(None, ge=0)
    pay_method: Optional[str] = Field(None, max_length=50)
    status_id: Optional[int] = Field(None, gt=0)

class PayRead(PayBase):
    id: int
    #Falta que implemente order schema jose
    #order: Optional[OrderRead] = None
    status: Optional[StatusRead] = None
    model_config = ConfigDict(from_attributes=True)
