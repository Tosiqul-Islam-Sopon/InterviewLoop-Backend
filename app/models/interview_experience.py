# models/interview_experience.py
from sqlalchemy import (
    String, Text, Boolean, Enum, ForeignKey
)
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
import enum


class DifficultyLevel(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class InterviewResult(str, enum.Enum):
    selected = "selected"
    rejected = "rejected"
    pending = "pending"


class ModerationStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class InterviewExperience(Base, TimestampMixin):
    __tablename__ = "interview_experiences"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    job_role_id: Mapped[int] = mapped_column(ForeignKey("job_roles.id"))
    interview_type_id: Mapped[int] = mapped_column(ForeignKey("interview_types.id"))

    experience_title: Mapped[str] = mapped_column(String(200))
    experience_details: Mapped[str] = mapped_column(Text)
    difficulty_level: Mapped[DifficultyLevel]
    result: Mapped[InterviewResult]
    interview_date: Mapped[date | None]
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=False)

    status: Mapped[ModerationStatus] = mapped_column(
        Enum(ModerationStatus), default=ModerationStatus.pending
    )

    user = relationship("User", back_populates="interview_experiences")
    company = relationship("Company", back_populates="interview_experiences")
    job_role = relationship("JobRole", back_populates="interview_experiences")
    interview_type = relationship("InterviewType", back_populates="interview_experiences")

    rounds = relationship("InterviewRound", cascade="all, delete")
    comments = relationship("Comment", cascade="all, delete")
    reactions = relationship("Reaction", cascade="all, delete")
    tags = relationship("Tag", secondary="interview_tags", back_populates="interviews")
