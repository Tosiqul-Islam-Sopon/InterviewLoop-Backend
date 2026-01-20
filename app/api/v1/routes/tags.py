from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.services.tag_service import TagService
from app.schemas.tag import TagCreate, TagUpdate, TagRead

router = APIRouter()

@router.post("/", response_model=TagRead)
def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_db)
):
    service = TagService(db)
    return service.create_tag(tag)

@router.get("/", response_model=List[TagRead])
def get_tags(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = TagService(db)
    return service.get_tags(skip=skip, limit=limit)

@router.get("/{tag_id}", response_model=TagRead)
def get_tag(
    tag_id: int,
    db: Session = Depends(get_db)
):
    service = TagService(db)
    return service.get_tag(tag_id)

@router.put("/{tag_id}", response_model=TagRead)
def update_tag(
    tag_id: int,
    tag_update: TagUpdate,
    db: Session = Depends(get_db)
):
    service = TagService(db)
    return service.update_tag(tag_id, tag_update)

@router.delete("/{tag_id}")
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db)
):
    service = TagService(db)
    service.delete_tag(tag_id)
    return {"message": "Tag deleted successfully"}