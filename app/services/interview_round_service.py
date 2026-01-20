from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from app.models.interview_round import InterviewRound
from app.schemas.interview_round import InterviewRoundCreate, InterviewRoundUpdate

class InterviewRoundService:
    def __init__(self, db: Session):
        self.db = db

    def create_interview_round(self, interview_round: InterviewRoundCreate) -> InterviewRound:
        existing = self.db.query(InterviewRound).filter(InterviewRound.name == interview_round.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Interview round already exists")
        
        db_interview_round = InterviewRound(**interview_round.model_dump())
        self.db.add(db_interview_round)
        self.db.commit()
        self.db.refresh(db_interview_round)
        return db_interview_round

    def get_interview_round(self, interview_round_id: int) -> InterviewRound:
        interview_round = self.db.query(InterviewRound).filter(InterviewRound.id == interview_round_id).first()
        if not interview_round:
            raise HTTPException(status_code=404, detail="Interview round not found")
        return interview_round

    def get_interview_rounds(self, skip: int = 0, limit: int = 100) -> List[InterviewRound]:
        return self.db.query(InterviewRound).offset(skip).limit(limit).all()

    def update_interview_round(self, interview_round_id: int, interview_round_update: InterviewRoundUpdate) -> InterviewRound:
        interview_round = self.get_interview_round(interview_round_id)
        
        update_data = interview_round_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(interview_round, field, value)
        
        self.db.commit()
        self.db.refresh(interview_round)
        return interview_round

    def delete_interview_round(self, interview_round_id: int) -> bool:
        interview_round = self.get_interview_round(interview_round_id)
        self.db.delete(interview_round)
        self.db.commit()
        return True