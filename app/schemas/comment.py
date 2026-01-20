from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    interview_experience_id: int
    comment_text: str

class CommentUpdate(BaseModel):
    comment_text: str | None = None

class CommentRead(BaseModel):
    id: int
    interview_experience_id: int
    user_id: int
    comment_text: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True