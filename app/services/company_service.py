from sqlalchemy.orm import Session
from app.models.company import Company as CompanyModel
from app.schemas.company import CompanyCreate, CompanyUpdate
from fastapi import HTTPException, status
from typing import List, Optional

class CompanyService:
    def __init__(self, db: Session):
        self.db = db

    # Create company
    def create_company(self, company_data: CompanyCreate):
        existing = self.db.query(CompanyModel).filter(CompanyModel.name == company_data.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Company already exists")
        new_company = CompanyModel(**company_data.dict())
        self.db.add(new_company)
        self.db.commit()
        self.db.refresh(new_company)
        return new_company

    # List companies
    def list_companies(self, active_only: bool = True) -> List[CompanyModel]:
        query = self.db.query(CompanyModel)
        if active_only:
            query = query.filter(CompanyModel.is_active == True)
        return query.all()

    # Get single company
    def get_company(self, company_id: int) -> CompanyModel:
        company = self.db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return company

    # Update company
    def update_company(self, company_id: int, company_data: CompanyUpdate) -> CompanyModel:
        company = self.get_company(company_id)
        for key, value in company_data.dict(exclude_unset=True).items():
            setattr(company, key, value)
        self.db.commit()
        self.db.refresh(company)
        return company

    # Soft delete company
    def delete_company(self, company_id: int):
        company = self.get_company(company_id)
        company.is_active = False
        self.db.commit()
        return
