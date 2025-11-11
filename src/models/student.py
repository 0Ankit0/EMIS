"""Student model for EMIS."""
from datetime import datetime, date
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4

from sqlalchemy import String, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class StudentStatus(str, Enum):
    """Student status enumeration."""

    APPLICANT = "applicant"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    WITHDRAWN = "withdrawn"
    GRADUATED = "graduated"
    ALUMNI = "alumni"


class Gender(str, Enum):
    """Gender enumeration."""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class Student(Base):
    """Student model representing a student in the system."""

    __tablename__ = "students"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    student_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[Optional[Gender]] = mapped_column(String(30), nullable=True)
    nationality: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Emergency contact
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    emergency_contact_relationship: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )

    # Academic info
    status: Mapped[StudentStatus] = mapped_column(
        String(20), default=StudentStatus.APPLICANT, index=True
    )
    admission_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    graduation_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    degree_earned: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    honors: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # User account reference
    user_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    enrollments: Mapped[List["Enrollment"]] = relationship(
        "Enrollment", back_populates="student", lazy="selectin"
    )
    academic_records: Mapped[List["AcademicRecord"]] = relationship(
        "AcademicRecord", back_populates="student", lazy="selectin"
    )
    attendance_records: Mapped[List["Attendance"]] = relationship(
        "Attendance", back_populates="student", lazy="selectin"
    )
    marks: Mapped[List["Marks"]] = relationship(
        "Marks", back_populates="student", lazy="selectin"
    )
    result_sheets: Mapped[List["ResultSheet"]] = relationship(
        "ResultSheet", back_populates="student", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Student(id={self.id}, student_number={self.student_number}, name={self.first_name} {self.last_name})>"

    @property
    def full_name(self) -> str:
        """Get student's full name."""
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return " ".join(parts)
