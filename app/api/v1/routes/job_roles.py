from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.job_role import JobRoleCreate, JobRoleUpdate, JobRoleRead
from app.services.job_role_service import JobRoleService
from app.core.auth import get_current_admin
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=JobRoleRead, status_code=status.HTTP_201_CREATED)
def create_job_role(
    job_role: JobRoleCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    service = JobRoleService(db)
    return service.create_job_role(job_role)


@router.get("/", response_model=List[JobRoleRead])
def get_job_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = JobRoleService(db)
    return service.get_job_roles(skip, limit)


@router.get("/{job_role_id}", response_model=JobRoleRead)
def get_job_role(
    job_role_id: int,
    db: Session = Depends(get_db)
):
    service = JobRoleService(db)
    job_role = service.get_job_role(job_role_id)
    if not job_role:
        raise HTTPException(status_code=404, detail="Job role not found")
    return job_role


@router.put("/{job_role_id}", response_model=JobRoleRead)
def update_job_role(
    job_role_id: int,
    job_role_update: JobRoleUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    service = JobRoleService(db)
    job_role = service.update_job_role(job_role_id, job_role_update)
    if not job_role:
        raise HTTPException(status_code=404, detail="Job role not found")
    return job_role


@router.delete("/{job_role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_role(
    job_role_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    service = JobRoleService(db)
    if not service.delete_job_role(job_role_id):
        raise HTTPException(status_code=404, detail="Job role not found")