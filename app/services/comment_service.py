from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate

class CommentService:
    def __init__(self, db: Session):
        self.db = db

    def create_comment(self, comment: CommentCreate, user_id: int) -> Comment:
        db_comment = Comment(
            user_id=user_id,
            **comment.model_dump()
        )
        self.db.add(db_comment)
        self.db.commit()
        self.db.refresh(db_comment)
        return db_comment

    def get_comment(self, comment_id: int) -> Comment:
        comment = self.db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment

    def get_comments_by_experience(self, interview_experience_id: int) -> List[Comment]:
        return self.db.query(Comment).filter(
            Comment.interview_experience_id == interview_experience_id
        ).all()

    def update_comment(self, comment_id: int, comment_update: CommentUpdate, user_id: int) -> Comment:
        comment = self.get_comment(comment_id)
        
        if comment.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this comment")
        
        update_data = comment_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(comment, field, value)
        
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete_comment(self, comment_id: int, user_id: int) -> bool:
        comment = self.get_comment(comment_id)
        
        if comment.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
        
        self.db.delete(comment)
        self.db.commit()
        return True