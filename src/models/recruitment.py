"""Recruitment model for EMIS."""
from datetime import datetime, date
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4

from sqlalchemy import String, Date, DateTime, Text, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class JobApplicationStatus(str, Enum):
    """Job application status enumeration."""

    RECEIVED = "received"
    SCREENING = "screening"
    SHORTLISTED = "shortlisted"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEWED = "interviewed"
    OFFERED = "offered"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class JobPostingStatus(str, Enum):
    """Job posting status enumeration."""
    
    DRAFT = "draft"
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class JobPosting(Base):
    """Job posting model for recruitment."""
    
    __tablename__ = "job_postings"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    job_title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    department: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    job_description: Mapped[str] = mapped_column(Text, nullable=False)
    requirements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Position details
    employment_type: Mapped[str] = mapped_column(String(20), nullable=False)
    number_of_positions: Mapped[int] = mapped_column(default=1)
    
    # Compensation
    salary_min: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    salary_max: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    
    # Dates
    posting_date: Mapped[date] = mapped_column(Date, default=date.today, index=True)
    application_deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Status
    status: Mapped[JobPostingStatus] = mapped_column(
        String(20), default=JobPostingStatus.DRAFT, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Contact
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Posted by
    posted_by: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    applications: Mapped[List["JobApplication"]] = relationship(
        "JobApplication", back_populates="job_posting", lazy="selectin"
    )
    poster: Mapped[Optional["Employee"]] = relationship("Employee", lazy="selectin")
    
    def __repr__(self) -> str:
        return f"<JobPosting(id={self.id}, title={self.job_title}, status={self.status})>"


class JobApplication(Base):
    """Job application model for recruitment applications."""

    __tablename__ = "job_applications"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    # Job posting
    job_posting_id: Mapped[UUID] = mapped_column(
        ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    # Applicant details
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Expected compensation
    expected_salary: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    
    # Application details
    application_date: Mapped[date] = mapped_column(Date, default=date.today, index=True)
    resume_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    cover_letter: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Status tracking
    status: Mapped[JobApplicationStatus] = mapped_column(
        String(30), default=JobApplicationStatus.RECEIVED, index=True
    )
    
    # Interview details
    interview_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    interview_feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Offer details
    offer_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    offered_salary: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    joining_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Employee record (if hired)
    employee_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    job_posting: Mapped["JobPosting"] = relationship(
        "JobPosting", back_populates="applications"
    )
    employee: Mapped[Optional["Employee"]] = relationship("Employee", lazy="selectin")
    
    def __repr__(self) -> str:
        return f"<JobApplication(id={self.id}, name={self.first_name} {self.last_name})>"
