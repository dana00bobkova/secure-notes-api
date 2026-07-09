from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models import Note, User
from app.rate_limit import note_create_rate_limiter
from app.schemas import NoteCreate, NoteRead, NoteUpdate
from app.services.audit_logger import log_audit_event

notes_router = APIRouter()


@notes_router.post(
    "/",
    response_model=NoteRead,
    status_code=status.HTTP_201_CREATED
)
def create_note(
    note_data: NoteCreate,
    request: Request,
    _rate_limit: None = Depends(note_create_rate_limiter),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_note = Note(
        title=note_data.title,
        content=note_data.content,
        owner_id=current_user.id
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    log_audit_event(
        db=db,
        event_type="NOTE_CREATED",
        success=True,
        request=request,
        user_id=current_user.id,
        email=current_user.email,
        details=f"Note created with note_id={new_note.id}."
    )

    return new_note


@notes_router.get("/", response_model=list[NoteRead])
def list_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notes = (
        db.query(Note)
        .filter(Note.owner_id == current_user.id)
        .all()
    )

    return notes


@notes_router.get("/{note_id}", response_model=NoteRead)
def read_note(
    note_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.owner_id == current_user.id)
        .first()
    )

    if note is None:
        log_audit_event(
            db=db,
            event_type="UNAUTHORIZED_OR_MISSING_NOTE_READ",
            success=False,
            request=request,
            user_id=current_user.id,
            email=current_user.email,
            details=f"User tried to read note_id={note_id}, but it was missing or not owned by the user."
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found."
        )

    return note


@notes_router.put("/{note_id}", response_model=NoteRead)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.owner_id == current_user.id)
        .first()
    )

    if note is None:
        log_audit_event(
            db=db,
            event_type="UNAUTHORIZED_OR_MISSING_NOTE_UPDATE",
            success=False,
            request=request,
            user_id=current_user.id,
            email=current_user.email,
            details=f"User tried to update note_id={note_id}, but it was missing or not owned by the user."
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found."
        )

    update_data = note_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(note, field, value)

    db.commit()
    db.refresh(note)

    log_audit_event(
        db=db,
        event_type="NOTE_UPDATED",
        success=True,
        request=request,
        user_id=current_user.id,
        email=current_user.email,
        details=f"Note updated with note_id={note.id}."
    )

    return note


@notes_router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_note(
    note_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.owner_id == current_user.id)
        .first()
    )

    if note is None:
        log_audit_event(
            db=db,
            event_type="UNAUTHORIZED_OR_MISSING_NOTE_DELETE",
            success=False,
            request=request,
            user_id=current_user.id,
            email=current_user.email,
            details=f"User tried to delete note_id={note_id}, but it was missing or not owned by the user."
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found."
        )

    db.delete(note)
    db.commit()

    log_audit_event(
        db=db,
        event_type="NOTE_DELETED",
        success=True,
        request=request,
        user_id=current_user.id,
        email=current_user.email,
        details=f"Note deleted with note_id={note_id}."
    )

    return None
