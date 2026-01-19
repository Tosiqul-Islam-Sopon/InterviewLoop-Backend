from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate
from app.core.auth import get_current_admin
from app.services.company_service import CompanyService
from app.models.user import User

router = APIRouter()

# Create company
@router.post("/", response_model=CompanyRead)
def create_company(
    company: CompanyCreate, 
    db: Session = Depends(get_db), 
    admin: User = Depends(get_current_admin),
):
    service = CompanyService(db)
    return service.create_company(company)

# List all companies
@router.get("/", response_model=List[CompanyRead])
def list_companies(db: Session = Depends(get_db)):
    service = CompanyService(db)
    return service.list_companies()

# Get single company
@router.get("/{company_id}", response_model=CompanyRead)
def get_company(company_id: int, db: Session = Depends(get_db)):
    service = CompanyService(db)
    return service.get_company(company_id)

# Update company
@router.patch("/{company_id}", response_model=CompanyRead)
def update_company(
    company_id: int, 
    company_update: CompanyUpdate, 
    db: Session = Depends(get_db), 
    admin: User = Depends(get_current_admin),
):
    service = CompanyService(db)
    return service.update_company(company_id, company_update)

# Soft delete company
@router.delete("/{company_id}", status_code=204)
def delete_company(company_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin),):
    service = CompanyService(db)
    service.delete_company(company_id)
    return
