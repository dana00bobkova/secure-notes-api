from fastapi import FastAPI

from app.api.notes import notes_router
from app.auth.routes import auth_router
from app.database import Base, engine

# These imports make sure SQLAlchemy knows about all database tables.
from app.models.user import User
from app.models.note import Note
from app.models.audit_log import AuditLog

from app.api.admin import admin_router

app = FastAPI(
    title="Secure Notes API",
    description="A secure-by-design notes API with authentication, authorization, audit logging, and DevSecOps checks.",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(notes_router, prefix="/notes", tags=["Notes"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])


@app.get("/")
def root():
    return {
        "message": "Secure Notes API is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }