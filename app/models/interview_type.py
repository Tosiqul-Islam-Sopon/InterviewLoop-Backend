# models/interview_type.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class InterviewType(Base):
    __tablename__ = "interview_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    interview_experiences = relationship(
        "InterviewExperience", back_populates="interview_type"
    )
