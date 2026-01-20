from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from app.models.reaction import Reaction
from app.schemas.reaction import ReactionCreate, ReactionUpdate

class ReactionService:
    def __init__(self, db: Session):
        self.db = db

    def create_reaction(self, reaction: ReactionCreate, user_id: int) -> Reaction:
        # Check if reaction already exists
        existing = self.db.query(Reaction).filter(
            Reaction.interview_experience_id == reaction.interview_experience_id,
            Reaction.user_id == user_id,
            Reaction.reaction_type == reaction.reaction_type
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Reaction already exists")
        
        db_reaction = Reaction(
            user_id=user_id,
            **reaction.model_dump()
        )
        self.db.add(db_reaction)
        self.db.commit()
        self.db.refresh(db_reaction)
        return db_reaction

    def get_reaction(self, reaction_id: int) -> Reaction:
        reaction = self.db.query(Reaction).filter(Reaction.id == reaction_id).first()
        if not reaction:
            raise HTTPException(status_code=404, detail="Reaction not found")
        return reaction

    def get_reactions_by_experience(self, interview_experience_id: int) -> List[Reaction]:
        return self.db.query(Reaction).filter(
            Reaction.interview_experience_id == interview_experience_id
        ).all()

    def delete_reaction(self, reaction_id: int, user_id: int) -> bool:
        reaction = self.get_reaction(reaction_id)
        
        if reaction.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this reaction")
        
        self.db.delete(reaction)
        self.db.commit()
        return True

    def toggle_reaction(self, interview_experience_id: int, reaction_type: str, user_id: int) -> dict:
        existing = self.db.query(Reaction).filter(
            Reaction.interview_experience_id == interview_experience_id,
            Reaction.user_id == user_id,
            Reaction.reaction_type == reaction_type
        ).first()
        
        if existing:
            self.db.delete(existing)
            self.db.commit()
            return {"action": "removed", "reaction_id": existing.id}
        else:
            new_reaction = Reaction(
                interview_experience_id=interview_experience_id,
                user_id=user_id,
                reaction_type=reaction_type
            )
            self.db.add(new_reaction)
            self.db.commit()
            self.db.refresh(new_reaction)
            return {"action": "added", "reaction_id": new_reaction.id}