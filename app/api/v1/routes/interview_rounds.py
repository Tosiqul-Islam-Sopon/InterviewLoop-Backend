from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.services.interview_round_service import InterviewRoundService
from app.schemas.interview_round import InterviewRoundCreate, InterviewRoundUpdate, InterviewRoundRead

router = APIRouter()

@router.post("/", response_model=InterviewRoundRead)
def create_interview_round(
    interview_round: InterviewRoundCreate,
    db: Session = Depends(get_db)
):
    service = InterviewRoundService(db)
    return service.create_interview_round(interview_round)

@router.get("/", response_model=List[InterviewRoundRead])
def get_interview_rounds(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = InterviewRoundService(db)
    return service.get_interview_rounds(skip=skip, limit=limit)

@router.get("/{interview_round_id}", response_model=InterviewRoundRead)
def get_interview_round(
    interview_round_id: int,
    db: Session = Depends(get_db)
):
    service = InterviewRoundService(db)
    return service.get_interview_round(interview_round_id)

@router.put("/{interview_round_id}", response_model=InterviewRoundRead)
def update_interview_round(
    interview_round_id: int,
    interview_round_update: InterviewRoundUpdate,
    db: Session = Depends(get_db)
):
    service = InterviewRoundService(db)
    return service.update_interview_round(interview_round_id, interview_round_update)

@router.delete("/{interview_round_id}")
def delete_interview_round(
    interview_round_id: int,
    db: Session = Depends(get_db)
):
    service = InterviewRoundService(db)
    service.delete_interview_round(interview_round_id)
    return {"message": "Interview round deleted successfully"}