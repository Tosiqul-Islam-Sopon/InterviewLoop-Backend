from fastapi import APIRouter
from app.api.v1.routes import (
    auth, interviews, users, company, job_roles,
    interview_types, interview_experiences, tags,
    comments, reactions, interview_rounds
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(company.router, prefix="/companies", tags=["Companies"])
api_router.include_router(job_roles.router, prefix="/job-roles", tags=["Job Roles"])
api_router.include_router(interview_types.router, prefix="/interview-types", tags=["Interview Types"])
api_router.include_router(interview_rounds.router, prefix="/interview-rounds", tags=["Interview Rounds"])
api_router.include_router(tags.router, prefix="/tags", tags=["Tags"])
api_router.include_router(interview_experiences.router, prefix="/interview-experiences", tags=["Interview Experiences"])
api_router.include_router(comments.router, prefix="/comments", tags=["Comments"])
api_router.include_router(reactions.router, prefix="/reactions", tags=["Reactions"])
