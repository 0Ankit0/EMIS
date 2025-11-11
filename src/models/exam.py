"""Exam Models for EMIS"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Float, Boolean, Enum, Text
from sqlalchemy.orm import relationship
import enum
from src.database import Base


class ExamType(str, enum.Enum):
    """Enumeration for exam types"""
    INTERNAL = "internal"
    EXTERNAL = "external"
    MIDTERM = "midterm"
    FINAL = "final"
    ASSIGNMENT = "assignment"
    QUIZ = "quiz"
    PRACTICAL = "practical"
    VIVA = "viva"


class ExamStatus(str, enum.Enum):
    """Enumeration for exam status"""
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    POSTPONED = "postponed"


class Exam(Base):
    """Exam model for managing examinations"""
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    
    exam_name = Column(String(200), nullable=False)
    exam_type = Column(Enum(ExamType), nullable=False)
    exam_code = Column(String(50), unique=True, nullable=False, index=True)
    
    exam_date = Column(Date, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    
    max_marks = Column(Float, nullable=False)
    passing_marks = Column(Float, nullable=False)
    weightage_percentage = Column(Float, default=100.0)
    
    venue = Column(String(200), nullable=True)
    room_number = Column(String(50), nullable=True)
    
    instructions = Column(Text, nullable=True)
    syllabus_topics = Column(Text, nullable=True)
    
    status = Column(Enum(ExamStatus), default=ExamStatus.SCHEDULED, nullable=False)
    
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    course = relationship("Course", back_populates="exams")
    marks = relationship("Marks", back_populates="exam", cascade="all, delete-orphan")
    creator = relationship("User", foreign_keys=[created_by])
    
    def __repr__(self):
        return f"<Exam(id={self.id}, name={self.exam_name}, type={self.exam_type}, date={self.exam_date})>"


class ExamRoutine(Base):
    """Exam routine/timetable model for scheduling exams."""
    
    __tablename__ = "exam_routines"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Routine details
    routine_name = Column(String(200), nullable=False)
    routine_code = Column(String(50), unique=True, nullable=False, index=True)
    
    # Academic context
    academic_year = Column(String(20), nullable=False, index=True)
    semester = Column(Integer, nullable=False, index=True)
    exam_type = Column(Enum(ExamType), nullable=False)  # midterm, final, etc.
    
    # Period
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Status and publication
    is_published = Column(Boolean, default=False, nullable=False)
    published_at = Column(DateTime, nullable=True)
    published_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # General instructions
    general_instructions = Column(Text, nullable=True)
    
    # Tracking
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    exam_slots = relationship("ExamRoutineSlot", back_populates="routine", cascade="all, delete-orphan")
    creator = relationship("User", foreign_keys=[created_by])
    publisher = relationship("User", foreign_keys=[published_by])
    
    def __repr__(self):
        return f"<ExamRoutine(id={self.id}, name={self.routine_name}, year={self.academic_year})>"


class ExamRoutineSlot(Base):
    """Individual exam slots in the routine."""
    
    __tablename__ = "exam_routine_slots"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Routine reference
    routine_id = Column(Integer, ForeignKey("exam_routines.id", ondelete="CASCADE"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    
    # Slot details
    exam_date = Column(Date, nullable=False, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    
    # Venue details
    venue = Column(String(200), nullable=True)
    room_numbers = Column(Text, nullable=True)  # Comma-separated list
    seating_arrangement = Column(String(100), nullable=True)  # e.g., "Roll number wise"
    
    # Invigilators
    chief_invigilator_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    assistant_invigilators = Column(Text, nullable=True)  # JSON array of employee IDs
    
    # Instructions
    special_instructions = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    routine = relationship("ExamRoutine", back_populates="exam_slots")
    exam = relationship("Exam")
    chief_invigilator = relationship("Employee", foreign_keys=[chief_invigilator_id])
    
    def __repr__(self):
        return f"<ExamRoutineSlot(id={self.id}, date={self.exam_date}, exam_id={self.exam_id})>"


class ExamFormStatus(str, enum.Enum):
    """Exam form status enumeration."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    VERIFIED = "verified"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAYMENT_PENDING = "payment_pending"
    PAYMENT_COMPLETED = "payment_completed"


class ExamForm(Base):
    """External examination form filled by students."""
    
    __tablename__ = "exam_forms"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Form details
    form_number = Column(String(50), unique=True, nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    routine_id = Column(Integer, ForeignKey("exam_routines.id", ondelete="CASCADE"), nullable=False)
    
    # Academic context
    academic_year = Column(String(20), nullable=False, index=True)
    semester = Column(Integer, nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id", ondelete="SET NULL"), nullable=True)
    
    # Course registrations
    registered_courses = Column(Text, nullable=False)  # JSON array of course IDs
    
    # Student declaration
    is_regular_student = Column(Boolean, default=True, nullable=False)
    has_fee_dues = Column(Boolean, default=False, nullable=False)
    declaration_accepted = Column(Boolean, default=False, nullable=False)
    declaration_date = Column(DateTime, nullable=True)
    
    # Status workflow
    status = Column(Enum(ExamFormStatus), default=ExamFormStatus.DRAFT, nullable=False, index=True)
    
    # Verification
    verified_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    verification_remarks = Column(Text, nullable=True)
    
    # Approval
    approved_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    approval_remarks = Column(Text, nullable=True)
    
    # Payment
    exam_fee_amount = Column(Float, nullable=True)
    payment_id = Column(Integer, ForeignKey("payments.id", ondelete="SET NULL"), nullable=True)
    payment_date = Column(DateTime, nullable=True)
    
    # Hall ticket
    hall_ticket_number = Column(String(50), unique=True, nullable=True, index=True)
    hall_ticket_generated_at = Column(DateTime, nullable=True)
    
    # Timestamps
    submitted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    student = relationship("Student")
    routine = relationship("ExamRoutine")
    program = relationship("Program")
    verifier = relationship("User", foreign_keys=[verified_by])
    approver = relationship("User", foreign_keys=[approved_by])
    payment = relationship("Payment")
    
    def __repr__(self):
        return f"<ExamForm(id={self.id}, form_number={self.form_number}, student_id={self.student_id}, status={self.status})>"
