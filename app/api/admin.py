from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.auth.dependencies import admin_required
from app.config import settings
from app.database import get_db
from app.models import AuditLog, Note, User
from app.schemas import AuditLogRead, UserRead
from app.services.audit_logger import log_audit_event

admin_router = APIRouter()


@admin_router.get(
    "/audit-logs",
    response_model=list[AuditLogRead]
)
def list_audit_logs(
    current_admin: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    audit_logs = (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .all()
    )

    return audit_logs


@admin_router.get(
    "/users",
    response_model=list[UserRead]
)
def list_users(
    current_admin: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    users = (
        db.query(User)
        .order_by(User.id.asc())
        .all()
    )

    return users


@admin_router.patch(
    "/users/{user_id}/disable",
    response_model=UserRead
)
def disable_user(
    user_id: int,
    request: Request,
    current_admin: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    if user_id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admins cannot disable their own account."
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    user.is_active = False

    db.commit()
    db.refresh(user)

    log_audit_event(
        db=db,
        event_type="USER_DISABLED",
        success=True,
        request=request,
        user_id=current_admin.id,
        email=current_admin.email,
        details=f"Admin disabled user_id={user.id}."
    )

    return user


@admin_router.get("/system-health")
def admin_system_health(
    current_admin: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    user_count = db.query(User).count()
    active_user_count = db.query(User).filter(User.is_active == True).count()
    note_count = db.query(Note).count()
    audit_log_count = db.query(AuditLog).count()

    return {
        "status": "ok",
        "environment": settings.environment,
        "database": "connected",
        "users_total": user_count,
        "users_active": active_user_count,
        "notes_total": note_count,
        "audit_logs_total": audit_log_count
    }