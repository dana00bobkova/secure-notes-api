from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    success: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    details: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )