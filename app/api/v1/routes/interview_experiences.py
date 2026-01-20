from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.interview_experience_service import InterviewExperienceService
from app.schemas.interview_experience import InterviewExperienceCreate, InterviewExperienceUpdate, InterviewExperienceRead

router = APIRouter()

@router.post("/", response_model=InterviewExperienceRead)
def create_interview_experience(
    interview_experience: InterviewExperienceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = InterviewExperienceService(db)
    return service.create_interview_experience(interview_experience, current_user.id)

@router.get("/", response_model=List[InterviewExperienceRead])
def get_interview_experiences(
    skip: int = 0,
    limit: int = 100,
    my_experiences: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = InterviewExperienceService(db)
    user_id = current_user.id if my_experiences else None
    return service.get_interview_experiences(skip=skip, limit=limit, user_id=user_id)

@router.get("/{interview_experience_id}", response_model=InterviewExperienceRead)
def get_interview_experience(
    interview_experience_id: int,
    db: Session = Depends(get_db)
):
    service = InterviewExperienceService(db)
    return service.get_interview_experience(interview_experience_id)

@router.put("/{interview_experience_id}", response_model=InterviewExperienceRead)
def update_interview_experience(
    interview_experience_id: int,
    interview_experience_update: InterviewExperienceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = InterviewExperienceService(db)
    return service.update_interview_experience(interview_experience_id, interview_experience_update, current_user.id)

@router.delete("/{interview_experience_id}")
def delete_interview_experience(
    interview_experience_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = InterviewExperienceService(db)
    service.delete_interview_experience(interview_experience_id, current_user.id)
    return {"message": "Interview experience deleted successfully"}