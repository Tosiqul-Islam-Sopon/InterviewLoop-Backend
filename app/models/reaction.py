# models/reaction.py
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class Reaction(Base, TimestampMixin):
    __tablename__ = "reactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    interview_experience_id: Mapped[int] = mapped_column(
        ForeignKey("interview_experiences.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    reaction_type: Mapped[str] = mapped_column(String(20))  # like | helpful

    __table_args__ = (
        UniqueConstraint(
            "interview_experience_id", "user_id", "reaction_type",
            name="unique_reaction_per_user"
        ),
    )
