# models/company.py
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class Company(Base, TimestampMixin):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    industry: Mapped[str | None]
    location: Mapped[str | None]
    website: Mapped[str | None]
    logo_url: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    interview_experiences = relationship("InterviewExperience", back_populates="company")
