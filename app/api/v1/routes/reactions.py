from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.reaction_service import ReactionService
from app.schemas.reaction import ReactionCreate, ReactionRead

router = APIRouter()

@router.post("/", response_model=ReactionRead)
def create_reaction(
    reaction: ReactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ReactionService(db)
    return service.create_reaction(reaction, current_user.id)

@router.get("/experience/{interview_experience_id}", response_model=List[ReactionRead])
def get_reactions_by_experience(
    interview_experience_id: int,
    db: Session = Depends(get_db)
):
    service = ReactionService(db)
    return service.get_reactions_by_experience(interview_experience_id)

@router.post("/toggle")
def toggle_reaction(
    interview_experience_id: int,
    reaction_type: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ReactionService(db)
    return service.toggle_reaction(interview_experience_id, reaction_type, current_user.id)

@router.delete("/{reaction_id}")
def delete_reaction(
    reaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ReactionService(db)
    service.delete_reaction(reaction_id, current_user.id)
    return {"message": "Reaction deleted successfully"}