"""Enrollment model for EMIS."""
from datetime import datetime, date
from enum import Enum
from typing import Optional, TYPE_CHECKING, List
from uuid import UUID, uuid4

from sqlalchemy import String, Date, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.models.student import Student


class EnrollmentStatus(str, Enum):
    """Enrollment status enumeration."""

    ACTIVE = "active"
    SUSPENDED = "suspended"
    WITHDRAWN = "withdrawn"
    COMPLETED = "completed"
    DEFERRED = "deferred"


class Enrollment(Base):
    """Enrollment model representing a student's enrollment in a program."""

    __tablename__ = "enrollments"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    program_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    semester: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[EnrollmentStatus] = mapped_column(
        String(20), default=EnrollmentStatus.ACTIVE, index=True
    )

    # Dates
    enrollment_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    expected_completion_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    withdrawal_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Academic standing
    credits_enrolled: Mapped[Optional[int]] = mapped_column(nullable=True)
    credits_earned: Mapped[Optional[int]] = mapped_column(nullable=True, default=0)
    current_gpa: Mapped[Optional[float]] = mapped_column(Numeric(3, 2), nullable=True)
    cumulative_gpa: Mapped[Optional[float]] = mapped_column(Numeric(3, 2), nullable=True)

    # Additional info
    enrollment_type: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )  # full-time, part-time
    section: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    advisor_id: Mapped[Optional[UUID]] = mapped_column(nullable=True, index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    withdrawal_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="enrollments")
    marks: Mapped[List["Marks"]] = relationship(
        "Marks", back_populates="enrollment", lazy="selectin"
    )
    result_sheets: Mapped[List["ResultSheet"]] = relationship(
        "ResultSheet", back_populates="enrollment", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Enrollment(id={self.id}, student_id={self.student_id}, semester={self.semester}, status={self.status})>"

    @property
    def is_active(self) -> bool:
        """Check if enrollment is currently active."""
        return self.status == EnrollmentStatus.ACTIVE

    @property
    def credits_remaining(self) -> int:
        """Calculate remaining credits to earn."""
        if self.credits_enrolled and self.credits_earned:
            return max(0, self.credits_enrolled - self.credits_earned)
        return 0
