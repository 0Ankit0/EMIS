"""
Calendar models for EMIS
Manages examinations, holidays, programs, and events
"""
from datetime import datetime, date
from enum import Enum
from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Boolean, ForeignKey, Time, Enum as SQLEnum
from sqlalchemy.orm import relationship
from src.database import Base


class CalendarEventType(str, Enum):
    """Types of calendar events"""
    EXAMINATION = "examination"
    HOLIDAY = "holiday"
    PROGRAM = "program"
    EVENT = "event"
    ACADEMIC = "academic"
    ADMINISTRATIVE = "administrative"
    CULTURAL = "cultural"
    SPORTS = "sports"
    WORKSHOP = "workshop"
    SEMINAR = "seminar"
    MEETING = "meeting"


class CalendarEvent(Base):
    """Calendar Event model"""
    __tablename__ = "calendar_events"
    
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    event_type = Column(SQLEnum(CalendarEventType), nullable=False, index=True)
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time)
    end_time = Column(Time)
    location = Column(String(255))
    is_holiday = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    
    # For examinations
    exam_id = Column(Integer, ForeignKey("exams.id"))
    
    # For programs/events
    department_id = Column(Integer, ForeignKey("departments.id"))
    organizer_id = Column(Integer, ForeignKey("users.id"))
    
    # Metadata
    color = Column(String(7), default="#3B82F6")  # Hex color for UI
    icon = Column(String(50))
    tags = Column(Text)  # JSON array of tags
    
    # Relationships
    exam = relationship("Exam", back_populates="calendar_events")
    department = relationship("Department", foreign_keys=[department_id])
    organizer = relationship("User", foreign_keys=[organizer_id])
    attendees = relationship("CalendarAttendee", back_populates="event", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<CalendarEvent {self.title} ({self.event_type})>"


class CalendarAttendee(Base):
    """Calendar event attendees"""
    __tablename__ = "calendar_attendees"
    
    event_id = Column(Integer, ForeignKey("calendar_events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"))
    
    is_required = Column(Boolean, default=False)
    has_responded = Column(Boolean, default=False)
    response = Column(String(20))  # accepted, declined, tentative
    response_date = Column(DateTime)
    
    # Relationships
    event = relationship("CalendarEvent", back_populates="attendees")
    user = relationship("User")
    student = relationship("Student")
    
    def __repr__(self):
        return f"<CalendarAttendee {self.user_id} for {self.event_id}>"


class AcademicCalendar(Base):
    """Academic year calendar"""
    __tablename__ = "academic_calendars"
    
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    semester = Column(String(50))  # Fall, Spring, Summer
    
    # Important dates
    semester_start = Column(Date, nullable=False)
    semester_end = Column(Date, nullable=False)
    registration_start = Column(Date)
    registration_end = Column(Date)
    add_drop_deadline = Column(Date)
    midterm_start = Column(Date)
    midterm_end = Column(Date)
    final_exam_start = Column(Date)
    final_exam_end = Column(Date)
    grade_submission_deadline = Column(Date)
    
    is_published = Column(Boolean, default=False)
    
    # Relationships
    academic_year = relationship("AcademicYear")
    
    def __repr__(self):
        return f"<AcademicCalendar {self.semester}>"


class Holiday(Base):
    """Holiday model"""
    __tablename__ = "holidays"
    
    name = Column(String(255), nullable=False)
    date = Column(Date, nullable=False, index=True)
    description = Column(Text)
    is_national = Column(Boolean, default=False)
    is_religious = Column(Boolean, default=False)
    is_institutional = Column(Boolean, default=True)
    
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"))
    
    # Relationships
    academic_year = relationship("AcademicYear")
    
    def __repr__(self):
        return f"<Holiday {self.name} on {self.date}>"
