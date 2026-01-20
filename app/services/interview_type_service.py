from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from app.models.interview_type import InterviewType
from app.schemas.interview_type import InterviewTypeCreate, InterviewTypeUpdate

class InterviewTypeService:
    def __init__(self, db: Session):
        self.db = db

    def create_interview_type(self, interview_type: InterviewTypeCreate) -> InterviewType:
        existing = self.db.query(InterviewType).filter(InterviewType.name == interview_type.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Interview type already exists")
        
        db_interview_type = InterviewType(**interview_type.model_dump())
        self.db.add(db_interview_type)
        self.db.commit()
        self.db.refresh(db_interview_type)
        return db_interview_type

    def get_interview_type(self, interview_type_id: int) -> InterviewType:
        interview_type = self.db.query(InterviewType).filter(InterviewType.id == interview_type_id).first()
        if not interview_type:
            raise HTTPException(status_code=404, detail="Interview type not found")
        return interview_type

    def get_interview_types(self, skip: int = 0, limit: int = 100) -> List[InterviewType]:
        return self.db.query(InterviewType).offset(skip).limit(limit).all()

    def update_interview_type(self, interview_type_id: int, interview_type_update: InterviewTypeUpdate) -> InterviewType:
        interview_type = self.get_interview_type(interview_type_id)
        
        update_data = interview_type_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(interview_type, field, value)
        
        self.db.commit()
        self.db.refresh(interview_type)
        return interview_type

    def delete_interview_type(self, interview_type_id: int) -> bool:
        interview_type = self.get_interview_type(interview_type_id)
        self.db.delete(interview_type)
        self.db.commit()
        return True