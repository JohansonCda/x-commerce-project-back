from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from .category_schema import CategoryRead

class ProductBase(BaseModel):
    """Base fields for products"""
    name: str = Field(..., max_length=255, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Product price")
    stock: int = Field(..., ge=0, description="Inventory stock")
    bought: int = Field(0, ge=0, description="Times product has been sold")
    enable: bool = Field(default=True, description="Whether the product is enabled")
    category_id: int = Field(..., gt=0, description="Category ID")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

class ProductCreate(BaseModel):
    """Schema for creating new products"""
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    stock: int = Field(..., ge=0)
    bought: int = Field(0, ge=0)
    enable: bool = Field(default=True)
    category_id: int = Field(..., gt=0)

class ProductUpdate(BaseModel):
    """Schema for updating products"""
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)
    bought: Optional[int] = Field(None, ge=0)
    enable: Optional[bool] = None
    category_id: Optional[int] = Field(None, gt=0)

class ProductRead(ProductBase):
    """Complete product schema including read-only fields"""
    id: int
    category: Optional[CategoryRead] = None
    model_config = ConfigDict(from_attributes=True)
