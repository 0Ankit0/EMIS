"""Book Loss Models for EMIS"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean, Enum, Text
from sqlalchemy.orm import relationship
import enum
from src.database import Base


class LossStatus(str, enum.Enum):
    """Enumeration for book loss status"""
    REPORTED = "reported"
    UNDER_INVESTIGATION = "under_investigation"
    CONFIRMED = "confirmed"
    RESOLVED = "resolved"
    WAIVED = "waived"


class BookLoss(Base):
    """Book Loss model for tracking lost library books"""
    __tablename__ = "book_losses"

    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("issues.id", ondelete="CASCADE"), nullable=False)
    member_id = Column(Integer, nullable=False)  # Student or Employee ID
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    
    # Book details at time of loss
    book_title = Column(String(500), nullable=False)
    book_isbn = Column(String(20), nullable=True)
    book_price = Column(Float, nullable=False)
    
    # Loss details
    reported_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    loss_date = Column(DateTime, nullable=True)
    
    status = Column(Enum(LossStatus), default=LossStatus.REPORTED, nullable=False)
    
    # Fine calculation
    book_replacement_cost = Column(Float, nullable=False)  # Actual book price
    processing_fine = Column(Float, default=0.0, nullable=False)  # Extra fine
    total_fine = Column(Float, nullable=False)  # Total amount to pay
    
    # Payment tracking
    amount_paid = Column(Float, default=0.0, nullable=False)
    is_paid = Column(Boolean, default=False, nullable=False)
    paid_date = Column(DateTime, nullable=True)
    
    # Investigation details
    investigation_notes = Column(Text, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    reported_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    investigated_by = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    resolved_by = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    book = relationship("Book", back_populates="losses")
    reporter = relationship("User", foreign_keys=[reported_by])
    investigator = relationship("Employee", foreign_keys=[investigated_by])
    resolver = relationship("Employee", foreign_keys=[resolved_by])
    
    def __repr__(self):
        return f"<BookLoss(id={self.id}, book={self.book_title}, member_id={self.member_id}, fine={self.total_fine}, status={self.status})>"


class LostBookSettings(Base):
    """Settings for lost book fine calculation"""
    __tablename__ = "lost_book_settings"

    id = Column(Integer, primary_key=True, index=True)
    
    # Processing fine configuration
    processing_fine_percentage = Column(Float, default=20.0, nullable=False)  # % of book price
    minimum_processing_fine = Column(Float, default=50.0, nullable=False)
    maximum_processing_fine = Column(Float, default=500.0, nullable=False)
    
    # Grace period for reporting
    grace_period_days = Column(Integer, default=7, nullable=False)
    
    # Additional settings
    allow_waiver = Column(Boolean, default=True, nullable=False)
    waiver_requires_approval = Column(Boolean, default=True, nullable=False)
    
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def calculate_processing_fine(self, book_price: float) -> float:
        """Calculate processing fine based on book price"""
        percentage_fine = book_price * (self.processing_fine_percentage / 100)
        return max(
            self.minimum_processing_fine,
            min(percentage_fine, self.maximum_processing_fine)
        )
    
    def __repr__(self):
        return f"<LostBookSettings(id={self.id}, processing_fine={self.processing_fine_percentage}%)>"
