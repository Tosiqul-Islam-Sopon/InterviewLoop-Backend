from pydantic import BaseModel
from typing import Optional

# Request models
class JobRoleCreate(BaseModel):
    title: str
    level: Optional[str] = None

class JobRoleUpdate(BaseModel):
    title: Optional[str] = None
    level: Optional[str] = None

# Response model
class JobRoleRead(BaseModel):
    id: int
    title: str
    level: Optional[str]

    class Config:
        from_attributes = True