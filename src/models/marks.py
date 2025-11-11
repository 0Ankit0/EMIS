"""Marks and Evaluation Models for EMIS"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean, Enum, Text
from sqlalchemy.orm import relationship
import enum
from src.database import Base


class MarksStatus(str, enum.Enum):
    """Enumeration for marks status"""
    PENDING = "pending"
    SUBMITTED = "submitted"
    VERIFIED = "verified"
    PUBLISHED = "published"
    WITHHELD = "withheld"
    ABSENT = "absent"


class GradeType(str, enum.Enum):
    """Enumeration for grade types"""
    A_PLUS = "A+"
    A = "A"
    B_PLUS = "B+"
    B = "B"
    C_PLUS = "C+"
    C = "C"
    D = "D"
    F = "F"
    PASS = "P"
    FAIL = "F"
    INCOMPLETE = "I"
    WITHDRAWN = "W"


class Marks(Base):
    """Marks model for student evaluation"""
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False)
    
    marks_obtained = Column(Float, nullable=True)
    max_marks = Column(Float, nullable=False)
    
    grade = Column(Enum(GradeType), nullable=True)
    grade_points = Column(Float, nullable=True)
    
    status = Column(Enum(MarksStatus), default=MarksStatus.PENDING, nullable=False)
    is_absent = Column(Boolean, default=False, nullable=False)
    
    remarks = Column(Text, nullable=True)
    evaluator_comments = Column(Text, nullable=True)
    
    evaluated_by = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    evaluated_at = Column(DateTime, nullable=True)
    
    verified_by = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    
    published_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    student = relationship("Student", back_populates="marks")
    exam = relationship("Exam", back_populates="marks")
    enrollment = relationship("Enrollment", back_populates="marks")
    evaluator = relationship("Employee", foreign_keys=[evaluated_by])
    verifier = relationship("Employee", foreign_keys=[verified_by])
    
    def __repr__(self):
        return f"<Marks(id={self.id}, student_id={self.student_id}, exam_id={self.exam_id}, marks={self.marks_obtained}/{self.max_marks})>"
