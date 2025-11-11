"""Financial Aid Models for EMIS"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Float, Boolean, Enum, Text
from sqlalchemy.orm import relationship
import enum
from src.database import Base


class AidType(str, enum.Enum):
    """Types of financial aid"""
    SCHOLARSHIP = "scholarship"
    GRANT = "grant"
    FEE_WAIVER = "fee_waiver"
    MERIT_SCHOLARSHIP = "merit_scholarship"
    NEED_BASED = "need_based"
    SPORTS_SCHOLARSHIP = "sports_scholarship"
    MINORITY_SCHOLARSHIP = "minority_scholarship"
    SC_ST_SCHOLARSHIP = "sc_st_scholarship"
    OBC_SCHOLARSHIP = "obc_scholarship"
    GOVERNMENT_SCHOLARSHIP = "government_scholarship"
    INSTITUTIONAL_SCHOLARSHIP = "institutional_scholarship"
    LOAN = "loan"


class AidStatus(str, enum.Enum):
    """Status of financial aid application"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    DISBURSED = "disbursed"
    CANCELLED = "cancelled"


class Scholarship(Base):
    """Scholarship/Grant master definition"""
    __tablename__ = "scholarships"

    id = Column(Integer, primary_key=True, index=True)
    
    # Basic details
    scholarship_name = Column(String(200), nullable=False)
    scholarship_code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Type and provider
    aid_type = Column(Enum(AidType), nullable=False)
    provider = Column(String(200), nullable=False)  # Government/Institution/Private
    
    # Eligibility criteria
    eligibility_criteria = Column(Text, nullable=False)
    minimum_percentage = Column(Float, nullable=True)
    family_income_limit = Column(Float, nullable=True)
    category_eligibility = Column(String(100), nullable=True)  # SC/ST/OBC/General
    
    # Financial details
    amount = Column(Float, nullable=False)
    is_percentage_based = Column(Boolean, default=False, nullable=False)
    percentage_of_fee = Column(Float, nullable=True)
    
    # Limits
    max_students = Column(Integer, nullable=True)
    current_beneficiaries = Column(Integer, default=0, nullable=False)
    
    # Active period
    academic_year = Column(String(20), nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    
    # Application period
    application_start_date = Column(Date, nullable=True)
    application_end_date = Column(Date, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_renewable = Column(Boolean, default=False, nullable=False)
    
    # Documentation requirements
    required_documents = Column(Text, nullable=True)  # JSON array
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    applications = relationship("FinancialAid", back_populates="scholarship")
    
    def __repr__(self):
        return f"<Scholarship(id={self.id}, name={self.scholarship_name}, amount={self.amount})>"


class FinancialAid(Base):
    """Financial Aid Application and Tracking"""
    __tablename__ = "financial_aid"

    id = Column(Integer, primary_key=True, index=True)
    
    # Application details
    application_number = Column(String(50), unique=True, nullable=False, index=True)
    scholarship_id = Column(Integer, ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    # Application period
    academic_year = Column(String(20), nullable=False)
    semester = Column(Integer, nullable=True)
    
    # Status
    status = Column(Enum(AidStatus), default=AidStatus.DRAFT, nullable=False)
    
    # Eligibility verification
    verified_percentage = Column(Float, nullable=True)
    verified_family_income = Column(Float, nullable=True)
    verified_category = Column(String(100), nullable=True)
    is_eligible = Column(Boolean, default=False, nullable=False)
    
    # Financial details
    requested_amount = Column(Float, nullable=False)
    approved_amount = Column(Float, nullable=True)
    disbursed_amount = Column(Float, default=0.0, nullable=False)
    
    # Application data
    application_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    submitted_date = Column(DateTime, nullable=True)
    
    # Review workflow
    reviewed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    review_date = Column(DateTime, nullable=True)
    review_comments = Column(Text, nullable=True)
    
    # Approval workflow
    approved_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    approval_date = Column(DateTime, nullable=True)
    approval_comments = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Disbursement
    disbursement_date = Column(DateTime, nullable=True)
    disbursement_method = Column(String(50), nullable=True)  # bank_transfer, adjustment_in_fee
    disbursement_reference = Column(String(100), nullable=True)
    
    # Documents
    uploaded_documents = Column(Text, nullable=True)  # JSON array of file paths
    
    # Bill adjustment
    adjusted_bill_id = Column(Integer, ForeignKey("bills.id", ondelete="SET NULL"), nullable=True)
    adjustment_amount = Column(Float, default=0.0, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    scholarship = relationship("Scholarship", back_populates="applications")
    student = relationship("Student", back_populates="financial_aids")
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    approver = relationship("User", foreign_keys=[approved_by])
    adjusted_bill = relationship("Bill")
    
    def __repr__(self):
        return f"<FinancialAid(id={self.id}, application_number={self.application_number}, student_id={self.student_id}, status={self.status})>"


class AidApplication(Base):
    """Standalone aid application (for general applications)"""
    __tablename__ = "aid_applications"

    id = Column(Integer, primary_key=True, index=True)
    
    # Applicant details
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    # Application details
    application_type = Column(Enum(AidType), nullable=False)
    requested_amount = Column(Float, nullable=False)
    reason = Column(Text, nullable=False)
    
    # Supporting information
    family_income = Column(Float, nullable=True)
    parent_occupation = Column(String(200), nullable=True)
    siblings_in_education = Column(Integer, default=0, nullable=False)
    
    # Status
    status = Column(Enum(AidStatus), default=AidStatus.DRAFT, nullable=False)
    
    # Workflow
    submitted_date = Column(DateTime, nullable=True)
    processed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    processed_date = Column(DateTime, nullable=True)
    decision_comments = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    student = relationship("Student")
    processor = relationship("User", foreign_keys=[processed_by])
    
    def __repr__(self):
        return f"<AidApplication(id={self.id}, student_id={self.student_id}, type={self.application_type}, status={self.status})>"
