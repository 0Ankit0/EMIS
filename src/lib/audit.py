from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.lib.logging import get_logger


logger = get_logger(__name__)


class AuditAction(str, Enum):
    """Types of audit actions."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    ACCESS_DENIED = "access_denied"
    EXPORT = "export"
    IMPORT = "import"


class AuditLog(Base):
    """Audit log model for tracking all system actions."""

    __tablename__ = "audit_logs"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[Optional[UUID]] = mapped_column(nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    resource: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )

    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action={self.action}, resource={self.resource})>"


async def log_audit(
    db,
    user_id: Optional[UUID],
    action: AuditAction,
    resource: str,
    resource_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    status: str = "success",
) -> None:
    """
    Log an audit event to the database.

    Args:
        db: Database session
        user_id: ID of the user performing the action
        action: Type of action (create, read, update, delete, etc.)
        resource: Type of resource being accessed
        resource_id: ID of the specific resource
        details: Additional details about the action
        ip_address: IP address of the requester
        user_agent: User agent string
        status: Status of the action (success, failed)
    """
    try:
        audit_entry = AuditLog(
            user_id=user_id,
            action=action.value,
            resource=resource,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            status=status,
        )
        db.add(audit_entry)
        await db.commit()

        logger.info(
            f"Audit: user={user_id} action={action.value} resource={resource} "
            f"resource_id={resource_id} status={status}"
        )
    except Exception as e:
        logger.error(f"Failed to log audit entry: {e}", exc_info=True)
        await db.rollback()


# Alias for backward compatibility
audit_log = log_audit
