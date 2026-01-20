from pydantic import BaseModel

class InterviewTypeCreate(BaseModel):
    name: str

class InterviewTypeUpdate(BaseModel):
    name: str | None = None

class InterviewTypeRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True