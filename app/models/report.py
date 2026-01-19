# models/report.py
from sqlalchemy import Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin
import enum


class ReportStatus(str, enum.Enum):
    open = "open"
    reviewed = "reviewed"
    resolved = "resolved"


class Report(Base, TimestampMixin):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    reported_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    interview_experience_id: Mapped[int] = mapped_column(
        ForeignKey("interview_experiences.id")
    )
    reason: Mapped[str] = mapped_column(Text)
    status: Mapped[ReportStatus] = mapped_column(Enum(ReportStatus), default=ReportStatus.open)
