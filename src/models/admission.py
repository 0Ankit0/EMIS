"""Admission models for EMIS."""
from datetime import datetime, date
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import String, Date, DateTime, Text, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class ApplicationStatus(str, Enum):
    """Application status enumeration."""
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    SHORTLISTED = "shortlisted"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    APPROVED = "approved"
    REJECTED = "rejected"
    WAITLISTED = "waitlisted"
    OFFER_SENT = "offer_sent"
    OFFER_ACCEPTED = "offer_accepted"
    OFFER_DECLINED = "offer_declined"
    ADMITTED = "admitted"


class Application(Base):
    """Application model for admissions."""
    
    __tablename__ = "applications"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    application_number: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    
    # Applicant details
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    nationality: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Address
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Program applied for
    program_id: Mapped[UUID] = mapped_column(
        ForeignKey("programs.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    semester: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Previous education
    previous_education: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    previous_institution: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    marks_obtained: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    total_marks: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    percentage: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    
    # Application details
    application_date: Mapped[date] = mapped_column(Date, default=date.today, index=True)
    status: Mapped[ApplicationStatus] = mapped_column(
        String(30), default=ApplicationStatus.SUBMITTED, index=True
    )
    
    # Interview
    interview_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    interview_score: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    interview_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Documents
    documents_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    documents_uploaded: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Review
    reviewed_by: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    review_comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Approval
    approved_by: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )
    approved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    approval_comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Student record (if admitted)
    student_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("students.id", ondelete="SET NULL"), nullable=True
    )
    
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    program: Mapped["Program"] = relationship("Program", lazy="selectin")
    reviewer: Mapped[Optional["Employee"]] = relationship(
        "Employee", foreign_keys=[reviewed_by], lazy="selectin"
    )
    approver: Mapped[Optional["Employee"]] = relationship(
        "Employee", foreign_keys=[approved_by], lazy="selectin"
    )
    student: Mapped[Optional["Student"]] = relationship("Student", lazy="selectin")
    
    @property
    def full_name(self) -> str:
        """Get applicant's full name."""
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return " ".join(parts)
    
    def __repr__(self) -> str:
        return f"<Application(id={self.id}, number={self.application_number}, status={self.status})>"
