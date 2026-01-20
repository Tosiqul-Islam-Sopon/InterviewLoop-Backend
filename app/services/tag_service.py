from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate

class TagService:
    def __init__(self, db: Session):
        self.db = db

    def create_tag(self, tag: TagCreate) -> Tag:
        existing = self.db.query(Tag).filter(Tag.name == tag.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Tag already exists")
        
        db_tag = Tag(**tag.model_dump())
        self.db.add(db_tag)
        self.db.commit()
        self.db.refresh(db_tag)
        return db_tag

    def get_tag(self, tag_id: int) -> Tag:
        tag = self.db.query(Tag).filter(Tag.id == tag_id).first()
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        return tag

    def get_tags(self, skip: int = 0, limit: int = 100) -> List[Tag]:
        return self.db.query(Tag).offset(skip).limit(limit).all()

    def get_tag_by_name(self, name: str) -> Tag:
        tag = self.db.query(Tag).filter(Tag.name == name).first()
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        return tag

    def update_tag(self, tag_id: int, tag_update: TagUpdate) -> Tag:
        tag = self.get_tag(tag_id)
        
        update_data = tag_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tag, field, value)
        
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def delete_tag(self, tag_id: int) -> bool:
        tag = self.get_tag(tag_id)
        self.db.delete(tag)
        self.db.commit()
        return True