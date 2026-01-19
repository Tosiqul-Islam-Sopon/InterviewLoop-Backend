from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.job_role import JobRole
from app.schemas.job_role import JobRoleCreate, JobRoleUpdate


class JobRoleService:
    def __init__(self, db: Session):
        self.db = db

    def create_job_role(self, job_role: JobRoleCreate) -> JobRole:
        db_job_role = JobRole(**job_role.model_dump())
        self.db.add(db_job_role)
        self.db.commit()
        self.db.refresh(db_job_role)
        return db_job_role

    def get_job_role(self, job_role_id: int) -> Optional[JobRole]:
        return self.db.query(JobRole).filter(JobRole.id == job_role_id).first()

    def get_job_roles(self, skip: int = 0, limit: int = 100) -> List[JobRole]:
        return self.db.query(JobRole).offset(skip).limit(limit).all()

    def update_job_role(self, job_role_id: int, job_role_update: JobRoleUpdate) -> Optional[JobRole]:
        db_job_role = self.db.query(JobRole).filter(JobRole.id == job_role_id).first()
        if not db_job_role:
            return None
        
        update_data = job_role_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_job_role, field, value)
        
        self.db.commit()
        self.db.refresh(db_job_role)
        return db_job_role

    def delete_job_role(self, job_role_id: int) -> bool:
        db_job_role = self.db.query(JobRole).filter(JobRole.id == job_role_id).first()
        if not db_job_role:
            return False
        
        self.db.delete(db_job_role)
        self.db.commit()
        return True