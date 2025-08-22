from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class StatusBase(BaseModel):
    name: str = Field(..., max_length=100, description="Status name")
    enable: bool = Field(default=True, description="Whether the status is enabled")
    registered_at: Optional[datetime] = Field(None, alias="register", description="Registration timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updated", description="Last update timestamp")

class StatusCreate(BaseModel):
    name: str = Field(..., max_length=100)
    enable: bool = Field(default=True)

class StatusUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    enable: Optional[bool] = None

class StatusRead(StatusBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
