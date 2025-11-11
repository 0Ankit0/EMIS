"""Notification models for EMIS."""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import String, DateTime, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class NotificationChannel(str, Enum):
    """Notification channel enumeration."""
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"
    PUSH = "push"
    WHATSAPP = "whatsapp"


class NotificationStatus(str, Enum):
    """Notification status enumeration."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"


class NotificationPriority(str, Enum):
    """Notification priority enumeration."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class Notification(Base):
    """Notification model for multi-channel notifications."""
    
    __tablename__ = "notifications"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    # Recipient
    recipient_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    recipient_type: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True
    )  # student, employee, parent
    
    # Channel
    channel: Mapped[NotificationChannel] = mapped_column(
        String(20), nullable=False, index=True
    )
    
    # Content
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Priority
    priority: Mapped[NotificationPriority] = mapped_column(
        String(20), default=NotificationPriority.NORMAL
    )
    
    # Status
    status: Mapped[NotificationStatus] = mapped_column(
        String(20), default=NotificationStatus.PENDING, index=True
    )
    
    # Delivery tracking
    sent_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    delivered_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    read_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    failed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    
    # Error tracking
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(default=0)
    max_retries: Mapped[int] = mapped_column(default=3)
    
    # Additional data
    extra_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Template
    template_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("notification_templates.id", ondelete="SET NULL"), nullable=True
    )
    
    # Scheduled
    scheduled_for: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    
    # Sender
    sent_by: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    template: Mapped[Optional["NotificationTemplate"]] = relationship(
        "NotificationTemplate", lazy="selectin"
    )
    sender: Mapped[Optional["User"]] = relationship("User", lazy="selectin")
    
    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, channel={self.channel}, status={self.status})>"


class NotificationTemplate(Base):
    """Notification template model for reusable templates."""
    
    __tablename__ = "notification_templates"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    
    # Template content
    subject_template: Mapped[str] = mapped_column(String(500), nullable=False)
    message_template: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Channel
    channel: Mapped[NotificationChannel] = mapped_column(String(20), nullable=False)
    
    # Variables
    variables: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    def __repr__(self) -> str:
        return f"<NotificationTemplate(id={self.id}, code={self.code}, name={self.name})>"
