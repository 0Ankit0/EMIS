"""Academic Record model for EMIS."""
from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import String, DateTime, Text, ForeignKey, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.models.student import Student


class GradeScale(str, Enum):
    """Grade scale enumeration."""

    A_PLUS = "A+"
    A = "A"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B = "B"
    B_MINUS = "B-"
    C_PLUS = "C+"
    C = "C"
    C_MINUS = "C-"
    D = "D"
    F = "F"
    PASS = "P"
    FAIL = "FAIL"
    INCOMPLETE = "I"
    WITHDRAWN = "W"


class AcademicRecord(Base):
    """Academic record model for tracking student course performance."""

    __tablename__ = "academic_records"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    course_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    enrollment_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("enrollments.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # Course information
    course_code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    course_name: Mapped[str] = mapped_column(String(200), nullable=False)
    credits: Mapped[int] = mapped_column(Integer, nullable=False)
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    semester: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Grading
    grade: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    grade_points: Mapped[Optional[float]] = mapped_column(Numeric(3, 2), nullable=True)
    percentage: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    is_pass: Mapped[Optional[bool]] = mapped_column(nullable=True)

    # Attendance
    total_classes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    classes_attended: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    attendance_percentage: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)

    # Additional details
    instructor_id: Mapped[Optional[UUID]] = mapped_column(nullable=True, index=True)
    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_retake: Mapped[bool] = mapped_column(default=False)
    original_record_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("academic_records.id", ondelete="SET NULL"), nullable=True
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="academic_records")

    def __repr__(self) -> str:
        return f"<AcademicRecord(id={self.id}, student_id={self.student_id}, course={self.course_code}, grade={self.grade})>"

    @property
    def attendance_rate(self) -> Optional[float]:
        """Calculate attendance rate."""
        if self.total_classes and self.classes_attended is not None:
            return round((self.classes_attended / self.total_classes) * 100, 2)
        return None

    def calculate_grade_points(self) -> Optional[float]:
        """Calculate grade points based on grade."""
        grade_point_map = {
            "A+": 4.0,
            "A": 4.0,
            "A-": 3.7,
            "B+": 3.3,
            "B": 3.0,
            "B-": 2.7,
            "C+": 2.3,
            "C": 2.0,
            "C-": 1.7,
            "D": 1.0,
            "F": 0.0,
        }
        if self.grade:
            return grade_point_map.get(self.grade)
        return None
