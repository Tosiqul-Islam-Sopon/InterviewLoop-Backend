# models/tag.py
from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


interview_tags = Table(
    "interview_tags",
    Base.metadata,
    Column("interview_experience_id", ForeignKey("interview_experiences.id")),
    Column("tag_id", ForeignKey("tags.id")),
)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    interviews = relationship(
        "InterviewExperience",
        secondary=interview_tags,
        back_populates="tags",
    )
