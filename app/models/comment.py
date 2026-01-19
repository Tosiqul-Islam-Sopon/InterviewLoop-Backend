# models/comment.py
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    interview_experience_id: Mapped[int] = mapped_column(
        ForeignKey("interview_experiences.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    comment_text: Mapped[str] = mapped_column(Text)
