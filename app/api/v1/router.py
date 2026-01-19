from fastapi import APIRouter
from app.api.v1.routes import auth, interviews, users, company, job_roles

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(company.router, prefix="/companies", tags=["Companies"])
api_router.include_router(interviews.router, prefix="/interviews", tags=["Interviews"])
api_router.include_router(job_roles.router, prefix="/job-roles", tags=["Job Roles"])
