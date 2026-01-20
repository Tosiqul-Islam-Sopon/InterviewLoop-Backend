from pydantic import BaseModel

class InterviewRoundCreate(BaseModel):
    name: str

class InterviewRoundUpdate(BaseModel):
    name: str | None = None

class InterviewRoundRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True