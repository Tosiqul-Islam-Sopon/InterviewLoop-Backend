# models/job_role.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class JobRole(Base):
    __tablename__ = "job_roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), index=True)
    level: Mapped[str | None]  # intern | junior | mid | senior

    interview_experiences = relationship("InterviewExperience", back_populates="job_role")
