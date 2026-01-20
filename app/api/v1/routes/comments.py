from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.comment_service import CommentService
from app.schemas.comment import CommentCreate, CommentUpdate, CommentRead

router = APIRouter()

@router.post("/", response_model=CommentRead)
def create_comment(
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = CommentService(db)
    return service.create_comment(comment, current_user.id)

@router.get("/experience/{interview_experience_id}", response_model=List[CommentRead])
def get_comments_by_experience(
    interview_experience_id: int,
    db: Session = Depends(get_db)
):
    service = CommentService(db)
    return service.get_comments_by_experience(interview_experience_id)

@router.put("/{comment_id}", response_model=CommentRead)
def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = CommentService(db)
    return service.update_comment(comment_id, comment_update, current_user.id)

@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = CommentService(db)
    service.delete_comment(comment_id, current_user.id)
    return {"message": "Comment deleted successfully"}