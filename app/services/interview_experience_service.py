from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from app.models.interview_experience import InterviewExperience
from app.schemas.interview_experience import InterviewExperienceCreate, InterviewExperienceUpdate

class InterviewExperienceService:
    def __init__(self, db: Session):
        self.db = db

    def create_interview_experience(self, interview_experience: InterviewExperienceCreate, user_id: int) -> InterviewExperience:
        db_interview_experience = InterviewExperience(
            user_id=user_id,
            **interview_experience.model_dump()
        )
        self.db.add(db_interview_experience)
        self.db.commit()
        self.db.refresh(db_interview_experience)
        return db_interview_experience

    def get_interview_experience(self, interview_experience_id: int) -> InterviewExperience:
        interview_experience = self.db.query(InterviewExperience).filter(
            InterviewExperience.id == interview_experience_id
        ).first()
        if not interview_experience:
            raise HTTPException(status_code=404, detail="Interview experience not found")
        return interview_experience

    def get_interview_experiences(self, skip: int = 0, limit: int = 100, user_id: int = None) -> List[InterviewExperience]:
        query = self.db.query(InterviewExperience)
        if user_id:
            query = query.filter(InterviewExperience.user_id == user_id)
        return query.offset(skip).limit(limit).all()

    def update_interview_experience(self, interview_experience_id: int, interview_experience_update: InterviewExperienceUpdate, user_id: int) -> InterviewExperience:
        interview_experience = self.get_interview_experience(interview_experience_id)
        
        if interview_experience.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this interview experience")
        
        update_data = interview_experience_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(interview_experience, field, value)
        
        self.db.commit()
        self.db.refresh(interview_experience)
        return interview_experience

    def delete_interview_experience(self, interview_experience_id: int, user_id: int) -> bool:
        interview_experience = self.get_interview_experience(interview_experience_id)
        
        if interview_experience.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this interview experience")
        
        self.db.delete(interview_experience)
        self.db.commit()
        return True