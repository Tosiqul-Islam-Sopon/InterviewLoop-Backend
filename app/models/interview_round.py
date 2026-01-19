# models/interview_round.py
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class InterviewRound(Base):
    __tablename__ = "interview_rounds"

    id: Mapped[int] = mapped_column(primary_key=True)
    interview_experience_id: Mapped[int] = mapped_column(
        ForeignKey("interview_experiences.id", ondelete="CASCADE")
    )
    round_no: Mapped[int]
    round_type: Mapped[str]  # HR | Technical | Coding | Written
    round_details: Mapped[str] = mapped_column(Text)
