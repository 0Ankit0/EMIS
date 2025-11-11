"""Library Settings Models for EMIS"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, Text
from sqlalchemy.orm import relationship
import enum
from src.database import Base


class MemberType(str, enum.Enum):
    """Enumeration for library member types"""
    STUDENT = "student"
    FACULTY = "faculty"
    STAFF = "staff"
    ALUMNI = "alumni"
    GUEST = "guest"


class LibrarySettings(Base):
    """Library Settings model for configurable library parameters"""
    __tablename__ = "library_settings"

    id = Column(Integer, primary_key=True, index=True)
    member_type = Column(Enum(MemberType), unique=True, nullable=False, index=True)
    
    # Borrowing limits
    max_books_allowed = Column(Integer, default=3, nullable=False)
    borrowing_period_days = Column(Integer, default=14, nullable=False)
    
    # Fine configuration
    fine_per_day = Column(Float, default=5.0, nullable=False)
    grace_period_days = Column(Integer, default=0, nullable=False)
    max_fine_amount = Column(Float, default=500.0, nullable=False)
    
    # Reservation limits
    max_reservations = Column(Integer, default=2, nullable=False)
    reservation_hold_days = Column(Integer, default=3, nullable=False)
    
    # Renewal configuration
    max_renewals = Column(Integer, default=2, nullable=False)
    
    # Digital resource access
    digital_access_enabled = Column(Boolean, default=True, nullable=False)
    digital_download_limit = Column(Integer, default=10, nullable=False)
    
    is_active = Column(Boolean, default=True, nullable=False)
    
    description = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    updated_by = Column(Integer, nullable=True)
    
    def __repr__(self):
        return f"<LibrarySettings(id={self.id}, member_type={self.member_type}, max_books={self.max_books_allowed}, fine_per_day={self.fine_per_day})>"


class FineWaiver(Base):
    """Fine Waiver model for tracking fine exemptions"""
    __tablename__ = "fine_waivers"

    id = Column(Integer, primary_key=True, index=True)
    fine_id = Column(Integer, nullable=False)
    member_id = Column(Integer, nullable=False)
    
    original_amount = Column(Float, nullable=False)
    waived_amount = Column(Float, nullable=False)
    final_amount = Column(Float, nullable=False)
    
    reason = Column(Text, nullable=False)
    
    approved_by = Column(Integer, nullable=False)
    approved_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<FineWaiver(id={self.id}, fine_id={self.fine_id}, waived={self.waived_amount})>"
