from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum

class DifficultyLevel(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class InterviewResult(str, Enum):
    selected = "selected"
    rejected = "rejected"
    pending = "pending"

class ModerationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class InterviewExperienceCreate(BaseModel):
    company_id: int
    job_role_id: int
    interview_type_id: int
    experience_title: str
    experience_details: str
    difficulty_level: DifficultyLevel
    result: InterviewResult
    interview_date: date | None = None
    is_anonymous: bool = False

class InterviewExperienceUpdate(BaseModel):
    company_id: int | None = None
    job_role_id: int | None = None
    interview_type_id: int | None = None
    experience_title: str | None = None
    experience_details: str | None = None
    difficulty_level: DifficultyLevel | None = None
    result: InterviewResult | None = None
    interview_date: date | None = None
    is_anonymous: bool | None = None
    status: ModerationStatus | None = None

class InterviewExperienceRead(BaseModel):
    id: int
    user_id: int
    company_id: int
    job_role_id: int
    interview_type_id: int
    experience_title: str
    experience_details: str
    difficulty_level: DifficultyLevel
    result: InterviewResult
    interview_date: date | None
    is_anonymous: bool
    status: ModerationStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True