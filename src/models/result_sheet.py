"""Result Sheet Models for EMIS"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean, Enum, Text, JSON
from sqlalchemy.orm import relationship
import enum
from src.database import Base


class ResultStatus(str, enum.Enum):
    """Enumeration for result status"""
    DRAFT = "draft"
    GENERATED = "generated"
    VERIFIED = "verified"
    PUBLISHED = "published"
    WITHHELD = "withheld"
    CANCELLED = "cancelled"


class ResultType(str, enum.Enum):
    """Enumeration for result types"""
    SEMESTER = "semester"
    ANNUAL = "annual"
    CUMULATIVE = "cumulative"
    TRANSCRIPT = "transcript"
    PROVISIONAL = "provisional"
    FINAL = "final"


class ResultSheet(Base):
    """Result Sheet model for consolidated student results"""
    __tablename__ = "result_sheets"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False)
    
    result_type = Column(Enum(ResultType), nullable=False)
    academic_year = Column(String(20), nullable=False)
    semester = Column(Integer, nullable=True)
    
    total_marks_obtained = Column(Float, nullable=False, default=0.0)
    total_max_marks = Column(Float, nullable=False, default=0.0)
    percentage = Column(Float, nullable=True)
    
    cgpa = Column(Float, nullable=True)
    sgpa = Column(Float, nullable=True)
    
    grade = Column(String(10), nullable=True)
    division = Column(String(50), nullable=True)
    
    rank = Column(Integer, nullable=True)
    total_students = Column(Integer, nullable=True)
    
    is_passed = Column(Boolean, default=False, nullable=False)
    has_backlogs = Column(Boolean, default=False, nullable=False)
    backlog_count = Column(Integer, default=0, nullable=False)
    
    status = Column(Enum(ResultStatus), default=ResultStatus.DRAFT, nullable=False)
    
    marks_breakdown = Column(JSON, nullable=True)
    subject_wise_details = Column(JSON, nullable=True)
    
    internal_marks_total = Column(Float, default=0.0)
    external_marks_total = Column(Float, default=0.0)
    
    remarks = Column(Text, nullable=True)
    
    generated_by = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    generated_at = Column(DateTime, nullable=True)
    
    verified_by = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    
    published_by = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    published_at = Column(DateTime, nullable=True)
    
    result_file_path = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    student = relationship("Student", back_populates="result_sheets")
    enrollment = relationship("Enrollment", back_populates="result_sheets")
    generator = relationship("Employee", foreign_keys=[generated_by])
    verifier = relationship("Employee", foreign_keys=[verified_by])
    publisher = relationship("Employee", foreign_keys=[published_by])
    
    def __repr__(self):
        return f"<ResultSheet(id={self.id}, student_id={self.student_id}, type={self.result_type}, year={self.academic_year}, status={self.status})>"
