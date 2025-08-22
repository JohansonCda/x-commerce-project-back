from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ProductImageBase(BaseModel):
    """Base fields for product images"""
    url: str = Field(..., max_length=512, description="Image URL")
    alt: Optional[str] = Field(None, max_length=255, description="Alt text for the image")
    is_main: bool = Field(default=False, description="Is this the main image?")
    product_id: int = Field(..., gt=0, description="Product ID")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

class ProductImageCreate(BaseModel):
    """Schema for creating new product images"""
    url: str = Field(..., max_length=512)
    alt: Optional[str] = None
    is_main: bool = Field(default=False)
    product_id: int = Field(..., gt=0)

class ProductImageUpdate(BaseModel):
    """Schema for updating product images"""
    url: Optional[str] = Field(None, max_length=512)
    alt: Optional[str] = Field(None, max_length=255)
    is_main: Optional[bool] = None
    product_id: Optional[int] = Field(None, gt=0)

class ProductImageRead(ProductImageBase):
    """Complete product image schema including read-only fields"""
    id: int
    model_config = ConfigDict(from_attributes=True)
