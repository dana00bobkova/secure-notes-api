from fastapi import Request
from sqlalchemy.orm import Session

from app.models import AuditLog


def get_client_ip(request: Request | None) -> str | None:
    if request is None:
        return None

    if request.client is None:
        return None

    return request.client.host


def log_audit_event(
    db: Session,
    event_type: str,
    success: bool,
    request: Request | None = None,
    user_id: int | None = None,
    email: str | None = None,
    details: str | None = None
) -> AuditLog:
    audit_log = AuditLog(
        event_type=event_type,
        user_id=user_id,
        email=email,
        success=success,
        ip_address=get_client_ip(request),
        details=details
    )

    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)

    return audit_log