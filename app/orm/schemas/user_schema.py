from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class UserBase(BaseModel):
    """Base fields for users"""
    username: str = Field(..., max_length=100, description="Username")
    full_name: str = Field(..., description="Full name of the user")
    email: str = Field(..., max_length=100, description="Email address")
    password: str = Field(..., min_length=6, max_length=100, description="User password")
    phone: str = Field(..., max_length=15, description="Phone number")
    enable: bool = Field(default=True, description="Whether the user is enabled")
    is_admin: bool = Field(default=False, description="Whether the user is an admin")   
    register_at: Optional[datetime] = Field(None, alias="register", description="Registration date in ISO format")
    update_at: Optional[datetime] = Field(None, alias="updated", description="Last update date in ISO format")

class UserCreate(BaseModel):
    username: str = Field(..., max_length=100, description="Username")
    full_name: str = Field(..., description="Full name of the user")
    email: str = Field(..., max_length=100, description="Email address")
    password: str = Field(..., min_length=6, max_length=100, description="User password")
    phone: str = Field(..., max_length=15, description="Phone number")
    enable: bool = Field(default=True, description="Whether the user is enabled")
    is_admin: bool = Field(default=False, description="Whether the user is an admin")

class UserUpdate(BaseModel):
    """Schema for updating users"""
    username: Optional[str] = Field(None, max_length=100, description="Username")
    full_name: Optional[str] = Field(None, description="Full name of the user")
    email: Optional[str] = Field(None, max_length=100, description="Email address")
    password: Optional[str] = Field(None, min_length=6, max_length=100, description="User password")
    phone: Optional[str] = Field(None, max_length=15, description="Phone number")
    enable: Optional[bool] = None
    is_admin: Optional[bool] = None

class UserRead(UserBase):
    """Complete user schema including read-only fields"""
    id: int

    model_config = ConfigDict(from_attributes=True)