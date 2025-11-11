"""Academic Calendar Models for EMIS"""
from datetime import datetime, date
from enum import Enum
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Text, ForeignKey, Time
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from src.database import Base


class CalendarEventType(str, Enum):
    """Types of calendar events"""
    EXAMINATION = "examination"
    HOLIDAY = "holiday"
    SEMESTER_START = "semester_start"
    SEMESTER_END = "semester_end"
    REGISTRATION = "registration"
    ADMISSION = "admission"
    PROGRAM_EVENT = "program_event"
    ORIENTATION = "orientation"
    CONVOCATION = "convocation"
    WORKSHOP = "workshop"
    SEMINAR = "seminar"
    SPORTS = "sports"
    CULTURAL = "cultural"
    DEADLINE = "deadline"
    MEETING = "meeting"
    OTHER = "other"


class CalendarEventStatus(str, Enum):
    """Status of calendar events"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    POSTPONED = "postponed"


class AcademicCalendar(Base):
    """Main Academic Calendar Model"""
    __tablename__ = "academic_calendar"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic Information
    title = Column(String(500), nullable=False)
    description = Column(Text)
    event_type = Column(String(50), nullable=False)  # CalendarEventType
    
    # Date & Time Information
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    is_all_day = Column(Boolean, default=True)
    
    # Academic Context
    academic_year = Column(String(20))
    semester = Column(Integer)
    program_id = Column(Integer, ForeignKey("programs.id"))
    department_id = Column(Integer)
    
    # Event Details
    location = Column(String(500))
    venue = Column(String(500))
    organizer = Column(String(200))
    contact_person = Column(String(200))
    contact_email = Column(String(200))
    contact_phone = Column(String(20))
    
    # Status & Visibility
    status = Column(String(50), default=CalendarEventStatus.SCHEDULED)
    is_published = Column(Boolean, default=False)
    is_recurring = Column(Boolean, default=False)
    recurrence_rule = Column(Text)  # RRULE format for recurring events
    
    # Target Audience
    is_for_students = Column(Boolean, default=True)
    is_for_faculty = Column(Boolean, default=True)
    is_for_staff = Column(Boolean, default=False)
    is_for_parents = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    
    # Additional Information
    color_code = Column(String(20))  # For UI display (e.g., "#FF5733")
    icon = Column(String(50))  # Icon name for UI
    priority = Column(Integer, default=0)  # 0=normal, 1=high, 2=urgent
    
    # Links & Resources
    registration_url = Column(String(500))
    resource_links = Column(JSONB)  # {"pdf": "url", "form": "url"}
    
    # Related Records
    exam_id = Column(Integer, ForeignKey("exams.id"))
    exam_routine_id = Column(Integer)
    admission_batch_id = Column(Integer)
    
    # Notifications
    send_reminder = Column(Boolean, default=True)
    reminder_days_before = Column(Integer, default=1)
    reminder_sent = Column(Boolean, default=False)
    
    # Metadata
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    published_by = Column(Integer, ForeignKey("users.id"))
    published_at = Column(DateTime)
    
    # Cancellation/Postponement
    cancelled_at = Column(DateTime)
    cancelled_by = Column(Integer, ForeignKey("users.id"))
    cancellation_reason = Column(Text)
    postponed_to_date = Column(Date)
    
    # Attachments & Notes
    attachments = Column(JSONB)  # Array of attachment objects
    notes = Column(Text)
    
    # Relationships
    program = relationship("Program", foreign_keys=[program_id])
    exam = relationship("Exam", foreign_keys=[exam_id])
    
    def __repr__(self):
        return f"<AcademicCalendar(title='{self.title}', date={self.start_date})>"
    
    @property
    def is_upcoming(self) -> bool:
        """Check if event is upcoming"""
        return self.start_date > date.today()
    
    @property
    def is_today(self) -> bool:
        """Check if event is today"""
        return self.start_date == date.today()
    
    @property
    def is_past(self) -> bool:
        """Check if event is in the past"""
        end = self.end_date or self.start_date
        return end < date.today()
    
    @property
    def duration_days(self) -> int:
        """Calculate event duration in days"""
        if self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 1


class Holiday(Base):
    """Holiday Calendar Model"""
    __tablename__ = "holidays"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Holiday Information
    name = Column(String(200), nullable=False)
    description = Column(Text)
    holiday_date = Column(Date, nullable=False)
    
    # Holiday Type
    holiday_type = Column(String(50))  # national, religious, local, college
    is_restricted = Column(Boolean, default=False)  # Restricted holiday (optional)
    
    # Applicability
    academic_year = Column(String(20))
    is_for_students = Column(Boolean, default=True)
    is_for_faculty = Column(Boolean, default=True)
    is_for_staff = Column(Boolean, default=True)
    
    # Metadata
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Calendar reference
    calendar_event_id = Column(UUID(as_uuid=True), ForeignKey("academic_calendar.id"))
    
    def __repr__(self):
        return f"<Holiday(name='{self.name}', date={self.holiday_date})>"


class ImportantDate(Base):
    """Important Dates & Deadlines Model"""
    __tablename__ = "important_dates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Date Information
    title = Column(String(500), nullable=False)
    description = Column(Text)
    deadline_date = Column(Date, nullable=False)
    deadline_time = Column(Time)
    
    # Category
    category = Column(String(100))  # admission, registration, fee_payment, exam_form, etc.
    
    # Academic Context
    academic_year = Column(String(20))
    semester = Column(Integer)
    
    # Notification
    send_notification = Column(Boolean, default=True)
    notification_days = Column(Integer, default=3)  # Notify X days before
    
    # Metadata
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Calendar reference
    calendar_event_id = Column(UUID(as_uuid=True), ForeignKey("academic_calendar.id"))
    
    def __repr__(self):
        return f"<ImportantDate(title='{self.title}', date={self.deadline_date})>"


class CalendarSubscription(Base):
    """User Calendar Subscriptions (for personalized calendars)"""
    __tablename__ = "calendar_subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # User Information
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Subscription Preferences
    event_types = Column(JSONB)  # Array of event types to subscribe to
    programs = Column(JSONB)  # Array of program IDs
    departments = Column(JSONB)  # Array of department IDs
    
    # Notification Preferences
    email_notifications = Column(Boolean, default=True)
    sms_notifications = Column(Boolean, default=False)
    push_notifications = Column(Boolean, default=True)
    
    # iCal/Google Calendar Integration
    ical_token = Column(String(100), unique=True)
    ical_url = Column(String(500))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<CalendarSubscription(user_id={self.user_id})>"
