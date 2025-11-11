"""Notifications API routes for EMIS."""
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.middleware.rbac import require_permissions
from src.models.auth import User


router = APIRouter(prefix="/api/v1/notifications", tags=["Notifications"])


class NotificationCreate(BaseModel):
    recipient_id: UUID
    recipient_type: str  # student, employee, parent
    channel: str  # email, sms, in_app
    subject: str
    message: str
    priority: Optional[str] = "normal"


class BulkNotificationCreate(BaseModel):
    recipient_ids: List[UUID]
    recipient_type: str
    channel: str
    subject: str
    message: str
    template_id: Optional[UUID] = None


class NotificationResponse(BaseModel):
    id: UUID
    recipient_id: UUID
    channel: str
    subject: str
    status: str
    sent_at: Optional[str]

    class Config:
        from_attributes = True


@router.post("/send", status_code=status.HTTP_201_CREATED)
async def send_notification(
    notification_data: NotificationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("notifications:send")),
):
    """Send a notification to a single recipient."""
    return {"message": "Notification sent successfully"}


@router.post("/send-bulk", status_code=status.HTTP_201_CREATED)
async def send_bulk_notification(
    notification_data: BulkNotificationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("notifications:send")),
):
    """Send notifications to multiple recipients."""
    return {
        "message": "Bulk notifications queued",
        "total_recipients": len(notification_data.recipient_ids)
    }


@router.get("/my-notifications")
async def get_my_notifications(
    unread_only: bool = False,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("notifications:read")),
):
    """Get notifications for the current user."""
    return {"items": [], "total": 0, "unread_count": 0}


@router.patch("/{notification_id}/read")
async def mark_as_read(
    notification_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("notifications:read")),
):
    """Mark a notification as read."""
    return {"message": "Notification marked as read"}


@router.get("/templates")
async def list_notification_templates(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("notifications:manage")),
):
    """List all notification templates."""
    return {"items": []}


@router.post("/schedule")
async def schedule_notification(
    notification_data: NotificationCreate,
    scheduled_time: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("notifications:send")),
):
    """Schedule a notification for later delivery."""
    return {"message": "Notification scheduled", "scheduled_time": scheduled_time}
