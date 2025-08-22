from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class CategoryBase(BaseModel):
    """Base fields for categories"""
    name: str = Field(..., max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    enable: bool = Field(default=True, description="Whether the category is enabled")

class CategoryCreate(BaseModel):
    """Schema for creating new categories"""
    name: str = Field(..., max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    enable: bool = Field(default=True, description="Whether the category is enabled")

class CategoryUpdate(BaseModel):
    """Schema for updating categories"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    enable: Optional[bool] = None

class CategoryRead(CategoryBase):
    """Complete category schema including read-only fields"""
    id: int
    model_config = ConfigDict(from_attributes=True)
