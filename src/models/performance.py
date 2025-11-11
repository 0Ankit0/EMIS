"""Performance review model for EMIS."""
from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import String, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.models.employee import Employee


class ReviewStatus(str, Enum):
    """Review status enumeration."""

    DRAFT = "draft"
    SUBMITTED = "submitted"
    COMPLETED = "completed"
    ACKNOWLEDGED = "acknowledged"


class PerformanceReview(Base):
    """Performance review model for employee evaluations."""

    __tablename__ = "performance_reviews"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    employee_id: Mapped[UUID] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True
    )
    reviewer_id: Mapped[UUID] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True, index=True
    )
    
    # Review period
    review_period: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    review_year: Mapped[int] = mapped_column(nullable=False, index=True)
    
    # Ratings (1-5 scale)
    technical_skills: Mapped[Optional[float]] = mapped_column(Numeric(2, 1), nullable=True)
    communication_skills: Mapped[Optional[float]] = mapped_column(Numeric(2, 1), nullable=True)
    teamwork: Mapped[Optional[float]] = mapped_column(Numeric(2, 1), nullable=True)
    leadership: Mapped[Optional[float]] = mapped_column(Numeric(2, 1), nullable=True)
    productivity: Mapped[Optional[float]] = mapped_column(Numeric(2, 1), nullable=True)
    overall_rating: Mapped[Optional[float]] = mapped_column(Numeric(2, 1), nullable=True)
    
    # Feedback
    strengths: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    areas_for_improvement: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    goals_for_next_period: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reviewer_comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    employee_comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Status
    status: Mapped[ReviewStatus] = mapped_column(
        String(20), default=ReviewStatus.DRAFT, index=True
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    submitted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    
    def __repr__(self) -> str:
        return f"<PerformanceReview(id={self.id}, employee_id={self.employee_id}, period={self.review_period})>"
    
    def calculate_overall_rating(self) -> Optional[float]:
        """Calculate average overall rating from individual ratings."""
        ratings = [
            self.technical_skills,
            self.communication_skills,
            self.teamwork,
            self.leadership,
            self.productivity,
        ]
        valid_ratings = [r for r in ratings if r is not None]
        
        if not valid_ratings:
            return None
        
        return round(sum(valid_ratings) / len(valid_ratings), 1)
