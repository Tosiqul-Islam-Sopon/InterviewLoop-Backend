from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.services.interview_type_service import InterviewTypeService
from app.schemas.interview_type import InterviewTypeCreate, InterviewTypeUpdate, InterviewTypeRead

router = APIRouter()

@router.post("/", response_model=InterviewTypeRead)
def create_interview_type(
    interview_type: InterviewTypeCreate,
    db: Session = Depends(get_db)
):
    service = InterviewTypeService(db)
    return service.create_interview_type(interview_type)

@router.get("/", response_model=List[InterviewTypeRead])
def get_interview_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = InterviewTypeService(db)
    return service.get_interview_types(skip=skip, limit=limit)

@router.get("/{interview_type_id}", response_model=InterviewTypeRead)
def get_interview_type(
    interview_type_id: int,
    db: Session = Depends(get_db)
):
    service = InterviewTypeService(db)
    return service.get_interview_type(interview_type_id)

@router.put("/{interview_type_id}", response_model=InterviewTypeRead)
def update_interview_type(
    interview_type_id: int,
    interview_type_update: InterviewTypeUpdate,
    db: Session = Depends(get_db)
):
    service = InterviewTypeService(db)
    return service.update_interview_type(interview_type_id, interview_type_update)

@router.delete("/{interview_type_id}")
def delete_interview_type(
    interview_type_id: int,
    db: Session = Depends(get_db)
):
    service = InterviewTypeService(db)
    service.delete_interview_type(interview_type_id)
    return {"message": "Interview type deleted successfully"}