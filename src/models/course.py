"""Course and LMS-related models for EMIS."""
from datetime import datetime
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Boolean, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.models.student import Student
    from src.models.employee import Employee


# Association table for course enrollments
course_enrollments = Table(
    "course_enrollments",
    Base.metadata,
    Column("course_id", ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True),
    Column("student_id", ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
    Column("enrolled_at", DateTime(timezone=True), default=datetime.utcnow),
    Column("status", String(20), default="active"),
)


class CourseStatus(str, Enum):
    """Course status enumeration."""
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class Course(Base):
    """Course model for academic courses."""
    
    __tablename__ = "courses"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    course_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    course_name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    credits: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Instructor
    instructor_id: Mapped[UUID] = mapped_column(
        ForeignKey("employees.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    
    # Academic period
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    semester: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    
    # Course details
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    max_enrollment: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[CourseStatus] = mapped_column(
        String(20), default=CourseStatus.DRAFT, index=True
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    instructor: Mapped["Employee"] = relationship("Employee", lazy="selectin")
    students: Mapped[List["Student"]] = relationship(
        secondary=course_enrollments, back_populates="courses", lazy="selectin"
    )
    assignments: Mapped[List["Assignment"]] = relationship(
        "Assignment", back_populates="course", lazy="selectin"
    )
    schedules: Mapped[List["ClassSchedule"]] = relationship(
        "ClassSchedule", back_populates="course", lazy="selectin"
    )
    exams: Mapped[List["Exam"]] = relationship(
        "Exam", back_populates="course", lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<Course(id={self.id}, code={self.course_code}, name={self.course_name})>"


class AssignmentStatus(str, Enum):
    """Assignment status enumeration."""
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"


class Assignment(Base):
    """Assignment model for course assignments."""
    
    __tablename__ = "assignments"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    course_id: Mapped[UUID] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Dates
    assigned_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    # Grading
    max_marks: Mapped[int] = mapped_column(Integer, nullable=False)
    weightage: Mapped[Optional[float]] = mapped_column(nullable=True)
    
    status: Mapped[AssignmentStatus] = mapped_column(
        String(20), default=AssignmentStatus.DRAFT
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    course: Mapped["Course"] = relationship("Course", back_populates="assignments")
    submissions: Mapped[List["AssignmentSubmission"]] = relationship(
        "AssignmentSubmission", back_populates="assignment", lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<Assignment(id={self.id}, title={self.title})>"


class SubmissionStatus(str, Enum):
    """Submission status enumeration."""
    SUBMITTED = "submitted"
    GRADED = "graded"
    LATE = "late"
    RESUBMITTED = "resubmitted"


class AssignmentSubmission(Base):
    """Assignment submission model."""
    
    __tablename__ = "assignment_submissions"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    assignment_id: Mapped[UUID] = mapped_column(
        ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    student_id: Mapped[UUID] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    # Submission content
    submission_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    attachment_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Submission details
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    is_late: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Grading
    marks_obtained: Mapped[Optional[float]] = mapped_column(nullable=True)
    graded_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    graded_by: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    status: Mapped[SubmissionStatus] = mapped_column(
        String(20), default=SubmissionStatus.SUBMITTED
    )
    
    # Relationships
    assignment: Mapped["Assignment"] = relationship(
        "Assignment", back_populates="submissions"
    )
    student: Mapped["Student"] = relationship("Student", lazy="selectin")
    grader: Mapped[Optional["Employee"]] = relationship("Employee", lazy="selectin")
    
    def __repr__(self) -> str:
        return f"<AssignmentSubmission(id={self.id}, assignment_id={self.assignment_id})>"
