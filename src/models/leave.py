"""Leave model for EMIS."""
from datetime import datetime, date
from enum import Enum
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import String, Date, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.models.employee import Employee


class LeaveType(str, Enum):
    """Leave type enumeration."""

    CASUAL = "casual"
    SICK = "sick"
    ANNUAL = "annual"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    BEREAVEMENT = "bereavement"
    COMPENSATORY = "compensatory"
    UNPAID = "unpaid"


class LeaveStatus(str, Enum):
    """Leave status enumeration."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class Leave(Base):
    """Leave model for employee leave requests."""

    __tablename__ = "employee_leaves"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    employee_id: Mapped[UUID] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    # Leave details
    leave_type: Mapped[LeaveType] = mapped_column(String(20), nullable=False, index=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    number_of_days: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Status
    status: Mapped[LeaveStatus] = mapped_column(
        String(20), default=LeaveStatus.PENDING, index=True
    )
    
    # Approval workflow
    approved_by: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )
    approved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    approval_comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Rejection details
    rejected_by: Mapped[Optional[UUID]] = mapped_column(nullable=True)
    rejected_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Supporting documents
    document_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    employee: Mapped["Employee"] = relationship(
        "Employee", back_populates="leave_requests", foreign_keys=[employee_id]
    )
    approver: Mapped[Optional["Employee"]] = relationship(
        "Employee", foreign_keys=[approved_by]
    )
    
    def __repr__(self) -> str:
        return f"<Leave(id={self.id}, employee_id={self.employee_id}, type={self.leave_type}, status={self.status})>"
    
    @property
    def is_approved(self) -> bool:
        """Check if leave is approved."""
        return self.status == LeaveStatus.APPROVED
    
    @property
    def is_pending(self) -> bool:
        """Check if leave is pending."""
        return self.status == LeaveStatus.PENDING
