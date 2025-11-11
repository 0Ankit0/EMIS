"""
Event Management models for EMIS
Manages college events, registrations, budgets, and attendance
"""
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Numeric, Date, Enum as SQLEnum
from sqlalchemy.orm import relationship
from src.database import Base


class EventType(str, Enum):
    """Types of events"""
    CULTURAL = "cultural"
    SPORTS = "sports"
    TECHNICAL = "technical"
    WORKSHOP = "workshop"
    SEMINAR = "seminar"
    CONFERENCE = "conference"
    FEST = "fest"
    COMPETITION = "competition"
    CEREMONY = "ceremony"
    OTHER = "other"


class EventStatus(str, Enum):
    """Event status"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RegistrationStatus(str, Enum):
    """Event registration status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    WAITLISTED = "waitlisted"


class Event(Base):
    """Event model"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    event_type = Column(SQLEnum(EventType), nullable=False)
    status = Column(SQLEnum(EventStatus), default=EventStatus.DRAFT)
    
    # Date and time
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    registration_start = Column(DateTime)
    registration_end = Column(DateTime)
    
    # Location
    venue = Column(String(255))
    venue_details = Column(Text)
    
    # Capacity
    max_participants = Column(Integer)
    current_participants = Column(Integer, default=0)
    
    # Fees
    registration_fee = Column(Numeric(10, 2), default=0)
    is_paid_event = Column(Boolean, default=False)
    
    # Organizer details
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    coordinator_name = Column(String(255))
    coordinator_contact = Column(String(20))
    coordinator_email = Column(String(255))
    
    # Event details
    is_inter_college = Column(Boolean, default=False)
    requires_approval = Column(Boolean, default=True)
    is_published = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    
    # Media
    banner_url = Column(String(500))
    brochure_url = Column(String(500))
    gallery_urls = Column(Text)  # JSON array
    
    # Social
    tags = Column(Text)  # JSON array
    external_url = Column(String(500))
    
    # Relationships
    organizer = relationship("User", foreign_keys=[organizer_id])
    department = relationship("Department")
    registrations = relationship("EventRegistration", back_populates="event", cascade="all, delete-orphan")
    budgets = relationship("EventBudget", back_populates="event", cascade="all, delete-orphan")
    attendance_records = relationship("EventAttendance", back_populates="event", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Event {self.title} ({self.event_type})>"


class EventRegistration(Base):
    """Event registration model"""
    __tablename__ = "event_registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    registration_date = Column(DateTime, default=datetime.utcnow)
    status = Column(SQLEnum(RegistrationStatus), default=RegistrationStatus.PENDING)
    
    # Participant details
    participant_name = Column(String(255), nullable=False)
    participant_email = Column(String(255), nullable=False)
    participant_phone = Column(String(20))
    college_name = Column(String(255))  # For inter-college events
    
    # Additional fields
    team_name = Column(String(255))
    team_members = Column(Text)  # JSON array for team events
    remarks = Column(Text)
    
    # Payment
    payment_status = Column(String(50))
    payment_id = Column(String(255))
    payment_date = Column(DateTime)
    amount_paid = Column(Numeric(10, 2))
    
    # Approval
    approved_by_id = Column(Integer, ForeignKey("users.id"))
    approved_date = Column(DateTime)
    rejection_reason = Column(Text)
    
    # Certificate
    certificate_issued = Column(Boolean, default=False)
    certificate_url = Column(String(500))
    certificate_issued_date = Column(DateTime)
    
    # Relationships
    event = relationship("Event", back_populates="registrations")
    student = relationship("Student")
    user = relationship("User", foreign_keys=[user_id])
    approved_by = relationship("User", foreign_keys=[approved_by_id])
    
    def __repr__(self):
        return f"<EventRegistration {self.participant_name} for Event {self.event_id}>"


class EventBudget(Base):
    """Event budget model"""
    __tablename__ = "event_budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    
    category = Column(String(100), nullable=False)  # Venue, Food, Prizes, Marketing, etc.
    description = Column(Text)
    
    # Budget amounts
    estimated_amount = Column(Numeric(10, 2), nullable=False)
    approved_amount = Column(Numeric(10, 2))
    actual_amount = Column(Numeric(10, 2))
    
    # Status
    is_approved = Column(Boolean, default=False)
    approved_by_id = Column(Integer, ForeignKey("users.id"))
    approved_date = Column(DateTime)
    
    # Documentation
    invoice_number = Column(String(100))
    invoice_url = Column(String(500))
    receipt_url = Column(String(500))
    
    notes = Column(Text)
    
    # Relationships
    event = relationship("Event", back_populates="budgets")
    approved_by = relationship("User")
    
    def __repr__(self):
        return f"<EventBudget {self.category} for Event {self.event_id}>"


class EventAttendance(Base):
    """Event attendance model"""
    __tablename__ = "event_attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    registration_id = Column(Integer, ForeignKey("event_registrations.id"))
    
    # Attendance details
    participant_name = Column(String(255), nullable=False)
    check_in_time = Column(DateTime)
    check_out_time = Column(DateTime)
    is_present = Column(Boolean, default=False)
    
    # For multi-day events
    attendance_date = Column(Date)
    session_name = Column(String(255))
    
    # Feedback
    rating = Column(Integer)  # 1-5
    feedback = Column(Text)
    feedback_date = Column(DateTime)
    
    remarks = Column(Text)
    
    # Relationships
    event = relationship("Event", back_populates="attendance_records")
    registration = relationship("EventRegistration")
    
    def __repr__(self):
        return f"<EventAttendance {self.participant_name} for Event {self.event_id}>"
