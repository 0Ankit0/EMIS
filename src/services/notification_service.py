"""Notification service for EMIS."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.notification import Notification, NotificationTemplate, NotificationChannel, NotificationPriority
from src.lib.logging import get_logger

logger = get_logger(__name__)


class NotificationService:
    """Service for managing notifications."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_notification(
        self,
        recipient_id: UUID,
        title: str,
        message: str,
        channel: NotificationChannel,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        scheduled_for: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Notification:
        """Create a new notification."""
        notification = Notification(
            recipient_id=recipient_id,
            title=title,
            message=message,
            channel=channel,
            priority=priority,
            scheduled_for=scheduled_for or datetime.utcnow(),
            status="pending",
            metadata=metadata,
        )

        self.db.add(notification)
        await self.db.commit()
        await self.db.refresh(notification)

        logger.info(f"Notification created for user {recipient_id}: {title}")
        return notification

    async def create_from_template(
        self,
        recipient_id: UUID,
        template_code: str,
        variables: Dict[str, Any],
        channel: NotificationChannel,
        priority: NotificationPriority = NotificationPriority.NORMAL,
    ) -> Notification:
        """Create notification from template."""
        # Get template
        result = await self.db.execute(
            select(NotificationTemplate).where(
                and_(
                    NotificationTemplate.template_code == template_code,
                    NotificationTemplate.is_active == True
                )
            )
        )
        template = result.scalar_one_or_none()

        if not template:
            raise ValueError(f"Template {template_code} not found or inactive")

        # Replace variables in subject and body
        subject = template.subject
        body = template.body

        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            subject = subject.replace(placeholder, str(value))
            body = body.replace(placeholder, str(value))

        return await self.create_notification(
            recipient_id=recipient_id,
            title=subject,
            message=body,
            channel=channel,
            priority=priority,
            metadata={"template_code": template_code, "variables": variables}
        )

    async def send_notification(self, notification_id: UUID) -> Notification:
        """Send a notification."""
        result = await self.db.execute(
            select(Notification).where(Notification.id == notification_id)
        )
        notification = result.scalar_one_or_none()

        if not notification:
            raise ValueError(f"Notification {notification_id} not found")

        if notification.status == "sent":
            logger.warning(f"Notification {notification_id} already sent")
            return notification

        # Here you would integrate with actual notification services
        # For now, we'll just mark as sent
        try:
            # TODO: Implement actual sending logic based on channel
            if notification.channel == NotificationChannel.EMAIL:
                await self._send_email(notification)
            elif notification.channel == NotificationChannel.SMS:
                await self._send_sms(notification)
            elif notification.channel == NotificationChannel.PUSH:
                await self._send_push(notification)
            elif notification.channel == NotificationChannel.IN_APP:
                # In-app notifications are just stored
                pass

            notification.status = "sent"
            notification.sent_at = datetime.utcnow()

        except Exception as e:
            notification.status = "failed"
            notification.error_message = str(e)
            logger.error(f"Failed to send notification {notification_id}: {e}")

        await self.db.commit()
        await self.db.refresh(notification)

        return notification

    async def _send_email(self, notification: Notification):
        """Send email notification (placeholder)."""
        # TODO: Integrate with email service (SendGrid, AWS SES, etc.)
        logger.info(f"Would send email: {notification.title}")
        pass

    async def _send_sms(self, notification: Notification):
        """Send SMS notification (placeholder)."""
        # TODO: Integrate with SMS service (Twilio, AWS SNS, etc.)
        logger.info(f"Would send SMS: {notification.title}")
        pass

    async def _send_push(self, notification: Notification):
        """Send push notification (placeholder)."""
        # TODO: Integrate with push service (Firebase, OneSignal, etc.)
        logger.info(f"Would send push: {notification.title}")
        pass

    async def mark_as_read(self, notification_id: UUID, recipient_id: UUID) -> Notification:
        """Mark notification as read."""
        result = await self.db.execute(
            select(Notification).where(
                and_(
                    Notification.id == notification_id,
                    Notification.recipient_id == recipient_id
                )
            )
        )
        notification = result.scalar_one_or_none()

        if not notification:
            raise ValueError(f"Notification {notification_id} not found")

        notification.read_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(notification)

        return notification

    async def get_user_notifications(
        self,
        user_id: UUID,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Notification]:
        """Get notifications for a user."""
        query = select(Notification).where(Notification.recipient_id == user_id)

        if unread_only:
            query = query.where(Notification.read_at.is_(None))

        query = query.order_by(Notification.created_at.desc()).limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def send_bulk_notification(
        self,
        recipient_ids: List[UUID],
        title: str,
        message: str,
        channel: NotificationChannel,
        priority: NotificationPriority = NotificationPriority.NORMAL,
    ) -> List[Notification]:
        """Send notification to multiple recipients."""
        notifications = []

        for recipient_id in recipient_ids:
            notification = await self.create_notification(
                recipient_id=recipient_id,
                title=title,
                message=message,
                channel=channel,
                priority=priority
            )
            notifications.append(notification)

        # Queue for sending
        for notification in notifications:
            try:
                await self.send_notification(notification.id)
            except Exception as e:
                logger.error(f"Failed to send bulk notification {notification.id}: {e}")

        logger.info(f"Bulk notification sent to {len(recipient_ids)} recipients")
        return notifications

    async def create_template(
        self,
        template_code: str,
        name: str,
        subject: str,
        body: str,
        category: str,
        variables: Optional[List[str]] = None,
    ) -> NotificationTemplate:
        """Create a notification template."""
        # Check if template code already exists
        result = await self.db.execute(
            select(NotificationTemplate).where(
                NotificationTemplate.template_code == template_code
            )
        )
        if result.scalar_one_or_none():
            raise ValueError(f"Template {template_code} already exists")

        template = NotificationTemplate(
            template_code=template_code,
            name=name,
            subject=subject,
            body=body,
            category=category,
            variables=variables or [],
            is_active=True,
        )

        self.db.add(template)
        await self.db.commit()
        await self.db.refresh(template)

        logger.info(f"Template created: {template_code}")
        return template

    async def send_pending_notifications(self):
        """Send all pending notifications."""
        result = await self.db.execute(
            select(Notification).where(
                and_(
                    Notification.status == "pending",
                    Notification.scheduled_for <= datetime.utcnow()
                )
            )
        )
        notifications = list(result.scalars().all())

        for notification in notifications:
            try:
                await self.send_notification(notification.id)
            except Exception as e:
                logger.error(f"Failed to send scheduled notification {notification.id}: {e}")

        logger.info(f"Processed {len(notifications)} pending notifications")
