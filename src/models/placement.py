"""
Placement Management Models for EMIS
"""
from datetime import datetime, date
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import String, Date, DateTime, Numeric, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Company(Base):
    """Recruiting company model"""
    __tablename__ = "companies"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    # Company details
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100))
    website: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Contact information
    contact_person: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    address: Mapped[Optional[str]] = mapped_column(Text)
    
    # Company details
    description: Mapped[Optional[str]] = mapped_column(Text)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Status
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job_postings = relationship("JobPosting", back_populates="company", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Company(name='{self.name}')>"


class JobType(str, Enum):
    """Job types"""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    INTERNSHIP = "internship"
    CONTRACT = "contract"


class JobPosting(Base):
    """Job posting model"""
    __tablename__ = "placement_job_postings"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    company_id: Mapped[UUID] = mapped_column(ForeignKey("companies.id"), nullable=False)
    
    # Job details
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    job_type: Mapped[JobType] = mapped_column(String(50), nullable=False)
    
    # Eligibility
    required_cgpa: Mapped[Optional[float]] = mapped_column(Numeric(3, 2))
    eligible_programs: Mapped[Optional[str]] = mapped_column(Text)  # JSON array
    eligible_departments: Mapped[Optional[str]] = mapped_column(Text)  # JSON array
    
    # Compensation
    salary_min: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    salary_max: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(10), default="INR")
    
    # Location
    location: Mapped[Optional[str]] = mapped_column(String(255))
    is_remote: Mapped[bool] = mapped_column(default=False)
    
    # Vacancies
    total_positions: Mapped[int] = mapped_column(Integer, default=1)
    filled_positions: Mapped[int] = mapped_column(Integer, default=0)
    
    # Dates
    posted_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    application_deadline: Mapped[date] = mapped_column(Date, nullable=False)
    interview_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Status
    is_active: Mapped[bool] = mapped_column(default=True)
    is_published: Mapped[bool] = mapped_column(default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="job_postings")
    applications = relationship("PlacementApplication", back_populates="job", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<JobPosting(title='{self.title}', company='{self.company_id}')>"


class ApplicationStatus(str, Enum):
    """Application status"""
    SUBMITTED = "submitted"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEW_COMPLETED = "interview_completed"
    SELECTED = "selected"
    OFFER_MADE = "offer_made"
    OFFER_ACCEPTED = "offer_accepted"
    OFFER_REJECTED = "offer_rejected"


class PlacementApplication(Base):
    """Student application for job posting"""
    __tablename__ = "placement_applications"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    job_id: Mapped[UUID] = mapped_column(ForeignKey("placement_job_postings.id"), nullable=False, index=True)
    
    # Application details
    cover_letter: Mapped[Optional[str]] = mapped_column(Text)
    resume_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Status
    status: Mapped[ApplicationStatus] = mapped_column(String(50), default=ApplicationStatus.SUBMITTED, index=True)
    
    # Timestamps
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job = relationship("JobPosting", back_populates="applications")
    interviews = relationship("Interview", back_populates="application", cascade="all, delete-orphan")
    offer = relationship("PlacementOffer", back_populates="application", uselist=False)
    
    def __repr__(self) -> str:
        return f"<PlacementApplication(student='{self.student_id}', job='{self.job_id}')>"


class Interview(Base):
    """Interview model"""
    __tablename__ = "interviews"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    application_id: Mapped[UUID] = mapped_column(ForeignKey("placement_applications.id"), nullable=False)
    
    # Interview details
    interview_type: Mapped[str] = mapped_column(String(50), nullable=False)  # technical, hr, group, etc.
    interview_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    interview_time: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Location
    location: Mapped[Optional[str]] = mapped_column(String(255))
    is_online: Mapped[bool] = mapped_column(default=False)
    meeting_link: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Feedback
    feedback: Mapped[Optional[str]] = mapped_column(Text)
    rating: Mapped[Optional[int]] = mapped_column(Integer)  # 1-5
    
    # Status
    is_completed: Mapped[bool] = mapped_column(default=False)
    is_cleared: Mapped[Optional[bool]] = mapped_column()
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    application = relationship("PlacementApplication", back_populates="interviews")
    
    def __repr__(self) -> str:
        return f"<Interview(application='{self.application_id}', type='{self.interview_type}')>"


class PlacementOffer(Base):
    """Placement offer model"""
    __tablename__ = "placement_offers"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    
    application_id: Mapped[UUID] = mapped_column(ForeignKey("placement_applications.id"), nullable=False, unique=True)
    
    # Offer details
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    salary: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="INR")
    
    joining_date: Mapped[Optional[date]] = mapped_column(Date)
    location: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Offer letter
    offer_letter_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Status
    is_accepted: Mapped[Optional[bool]] = mapped_column()
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Timestamps
    offered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    application = relationship("PlacementApplication", back_populates="offer")
    
    def __repr__(self) -> str:
        return f"<PlacementOffer(application='{self.application_id}', salary={self.salary})>"
