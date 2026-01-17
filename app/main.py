from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router

# --- DB init ---
from app.db.base import Base
from app.db.session import engine
from app.models import User  # ensures User is loaded
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)  # <-- creates tables

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(api_router, prefix="/api/v1")

# health check
@app.get("/health")
def health_check():
    return {"status": "ok"}
