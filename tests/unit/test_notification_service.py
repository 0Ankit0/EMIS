"""Tests for Notification Service"""
import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.notification_service import NotificationService


@pytest.fixture
def notification_service():
    return NotificationService()


@pytest.mark.asyncio
async def test_send_email_notification(
    db_session: AsyncSession,
    notification_service: NotificationService
):
    """Test sending email notification"""
    notification_data = {
        "recipient": "user@example.com",
        "subject": "Test Notification",
        "body": "This is a test message",
        "type": "email"
    }
    
    notification = await notification_service.send_notification(
        db_session,
        **notification_data
    )
    
    assert notification is not None
    assert notification.recipient == "user@example.com"


@pytest.mark.asyncio
async def test_send_sms_notification(
    db_session: AsyncSession,
    notification_service: NotificationService
):
    """Test sending SMS notification"""
    notification_data = {
        "recipient": "1234567890",
        "message": "Test SMS",
        "type": "sms"
    }
    
    notification = await notification_service.send_sms(
        db_session,
        **notification_data
    )
    
    assert notification is not None


@pytest.mark.asyncio
async def test_send_push_notification(
    db_session: AsyncSession,
    notification_service: NotificationService
):
    """Test sending push notification"""
    notification_data = {
        "user_id": uuid4(),
        "title": "New Update",
        "message": "You have a new message",
        "type": "push"
    }
    
    notification = await notification_service.send_push(
        db_session,
        **notification_data
    )
    
    assert notification is not None


@pytest.mark.asyncio
async def test_get_user_notifications(
    db_session: AsyncSession,
    notification_service: NotificationService
):
    """Test getting user notifications"""
    user_id = uuid4()
    
    # Send notification
    await notification_service.send_notification(
        db_session,
        user_id=user_id,
        subject="Test",
        body="Test message",
        type="in_app"
    )
    
    notifications = await notification_service.get_user_notifications(
        db_session,
        user_id=user_id
    )
    
    assert len(notifications) >= 1


@pytest.mark.asyncio
async def test_mark_as_read(
    db_session: AsyncSession,
    notification_service: NotificationService
):
    """Test marking notification as read"""
    user_id = uuid4()
    
    notification = await notification_service.send_notification(
        db_session,
        user_id=user_id,
        subject="Test",
        body="Test",
        type="in_app"
    )
    
    success = await notification_service.mark_as_read(
        db_session,
        notification_id=notification.id
    )
    
    assert success is True


@pytest.mark.asyncio
async def test_send_bulk_notifications(
    db_session: AsyncSession,
    notification_service: NotificationService
):
    """Test sending bulk notifications"""
    user_ids = [uuid4() for _ in range(5)]
    
    count = await notification_service.send_bulk(
        db_session,
        user_ids=user_ids,
        subject="Announcement",
        body="Important announcement",
        type="email"
    )
    
    assert count == 5
