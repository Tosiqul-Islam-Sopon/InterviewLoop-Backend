from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

# Request models
class CompanyCreate(BaseModel):
    name: str
    industry: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    is_active: Optional[bool] = None

# Response model
class CompanyRead(BaseModel):
    id: int
    name: str
    industry: Optional[str]
    location: Optional[str]
    website: Optional[str]
    logo_url: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
