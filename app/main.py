from fastapi import FastAPI

from app.api import notes_router
from app.auth import auth_router
from app.database import Base, engine
from app.models import User, Note

app = FastAPI(
    title="Secure Notes API",
    version="0.1.0",
    description="A secure-by-design notes API with authentication, RBAC, testing, and DevSecOps scanning."
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Secure Notes API is running!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(notes_router, prefix="/notes", tags=["Notes"])
