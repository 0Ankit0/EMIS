"""Attendance model for EMIS."""
from datetime import datetime, date
from enum import Enum
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import String, Date, DateTime, Time, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.models.student import Student


class AttendanceStatus(str, Enum):
    """Attendance status enumeration."""

    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"
    LEAVE = "leave"


class Attendance(Base):
    """Attendance model for tracking student attendance."""

    __tablename__ = "attendance"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    course_id: Mapped[Optional[UUID]] = mapped_column(nullable=True, index=True)
    class_id: Mapped[Optional[UUID]] = mapped_column(nullable=True, index=True)

    # Attendance details
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    time_in: Mapped[Optional[datetime]] = mapped_column(Time, nullable=True)
    time_out: Mapped[Optional[datetime]] = mapped_column(Time, nullable=True)
    status: Mapped[AttendanceStatus] = mapped_column(
        String(20), nullable=False, default=AttendanceStatus.PRESENT, index=True
    )

    # Additional information
    academic_year: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, index=True)
    semester: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    period: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    room: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    instructor_id: Mapped[Optional[UUID]] = mapped_column(nullable=True, index=True)

    # Leave/absence details
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_excused: Mapped[bool] = mapped_column(default=False)
    excuse_document_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Tracking
    marked_by: Mapped[Optional[UUID]] = mapped_column(nullable=True)  # User who marked attendance
    marked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="attendance_records")

    def __repr__(self) -> str:
        return f"<Attendance(id={self.id}, student_id={self.student_id}, date={self.date}, status={self.status})>"

    @property
    def is_present(self) -> bool:
        """Check if student was present."""
        return self.status in [AttendanceStatus.PRESENT, AttendanceStatus.LATE]

    @property
    def duration_minutes(self) -> Optional[int]:
        """Calculate attendance duration in minutes."""
        if self.time_in and self.time_out:
            delta = datetime.combine(date.min, self.time_out) - datetime.combine(
                date.min, self.time_in
            )
            return int(delta.total_seconds() / 60)
        return None


class LeaveRequestStatus(str, Enum):
    """Leave request status enumeration."""
    
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class LeaveRequest(Base):
    """Leave request model for students to request leave from teachers."""
    
    __tablename__ = "leave_requests"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    # Request details
    student_id: Mapped[UUID] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    course_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    subject_teacher_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    
    # Leave period
    leave_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    leave_type: Mapped[str] = mapped_column(String(50), nullable=False)  # sick, personal, family, etc.
    
    # Request information
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    supporting_document_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Approval workflow
    status: Mapped[LeaveRequestStatus] = mapped_column(
        String(20), nullable=False, default=LeaveRequestStatus.PENDING, index=True
    )
    approved_by: Mapped[Optional[UUID]] = mapped_column(nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    student: Mapped["Student"] = relationship("Student")
    
    def __repr__(self) -> str:
        return f"<LeaveRequest(id={self.id}, student_id={self.student_id}, status={self.status})>"


class AttendanceSession(Base):
    """Attendance session for bulk attendance marking."""
    
    __tablename__ = "attendance_sessions"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    # Session details
    course_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    class_id: Mapped[Optional[UUID]] = mapped_column(nullable=True, index=True)
    instructor_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    
    # Session timing
    session_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    start_time: Mapped[datetime] = mapped_column(Time, nullable=False)
    end_time: Mapped[datetime] = mapped_column(Time, nullable=False)
    
    # Academic context
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    semester: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    period: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    room: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Tracking
    total_students: Mapped[int] = mapped_column(default=0)
    present_count: Mapped[int] = mapped_column(default=0)
    absent_count: Mapped[int] = mapped_column(default=0)
    late_count: Mapped[int] = mapped_column(default=0)
    leave_count: Mapped[int] = mapped_column(default=0)
    
    is_completed: Mapped[bool] = mapped_column(default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    def __repr__(self) -> str:
        return f"<AttendanceSession(id={self.id}, date={self.session_date}, course_id={self.course_id})>"
