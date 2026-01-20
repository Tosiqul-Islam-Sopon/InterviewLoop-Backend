from pydantic import BaseModel
from datetime import datetime

class ReactionCreate(BaseModel):
    interview_experience_id: int
    reaction_type: str

class ReactionUpdate(BaseModel):
    reaction_type: str | None = None

class ReactionRead(BaseModel):
    id: int
    interview_experience_id: int
    user_id: int
    reaction_type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True