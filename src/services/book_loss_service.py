"""Book Loss Service for EMIS"""
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from src.models.book_loss import BookLoss, LostBookSettings, LossStatus
from src.models.library import Book
from src.lib.logging import get_logger

logger = get_logger(__name__)


class BookLossService:
    """Service for managing lost library books"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_lost_book_settings(self) -> Optional[LostBookSettings]:
        """Get current lost book settings"""
        result = await self.db.execute(
            select(LostBookSettings).where(LostBookSettings.is_active == True).limit(1)
        )
        return result.scalar_one_or_none()
    
    async def report_lost_book(
        self,
        issue_id: int,
        member_id: int,
        book_id: int,
        book_title: str,
        book_isbn: Optional[str],
        book_price: float,
        loss_date: Optional[datetime] = None,
        reported_by: Optional[int] = None
    ) -> BookLoss:
        """Report a book as lost"""
        
        # Get settings
        settings = await self.get_lost_book_settings()
        if not settings:
            # Create default settings
            settings = LostBookSettings()
            self.db.add(settings)
            await self.db.commit()
        
        # Calculate fines
        processing_fine = settings.calculate_processing_fine(book_price)
        total_fine = book_price + processing_fine
        
        # Create loss record
        book_loss = BookLoss(
            issue_id=issue_id,
            member_id=member_id,
            book_id=book_id,
            book_title=book_title,
            book_isbn=book_isbn,
            book_price=book_price,
            loss_date=loss_date,
            book_replacement_cost=book_price,
            processing_fine=processing_fine,
            total_fine=total_fine,
            status=LossStatus.REPORTED,
            reported_by=reported_by
        )
        
        self.db.add(book_loss)
        await self.db.commit()
        await self.db.refresh(book_loss)
        
        logger.info(f"Reported lost book {book_title} (ID: {book_id}) for member {member_id}, fine: ₹{total_fine}")
        
        return book_loss
    
    async def investigate_loss(
        self,
        loss_id: int,
        investigator_id: int,
        notes: Optional[str] = None
    ) -> BookLoss:
        """Mark a book loss as under investigation"""
        result = await self.db.execute(
            select(BookLoss).where(BookLoss.id == loss_id)
        )
        book_loss = result.scalar_one_or_none()
        
        if not book_loss:
            raise ValueError(f"Book loss {loss_id} not found")
        
        book_loss.status = LossStatus.UNDER_INVESTIGATION
        book_loss.investigated_by = investigator_id
        book_loss.investigation_notes = notes
        
        await self.db.commit()
        await self.db.refresh(book_loss)
        
        logger.info(f"Book loss {loss_id} under investigation by {investigator_id}")
        
        return book_loss
    
    async def confirm_loss(
        self,
        loss_id: int,
        confirmed_by: int,
        resolution_notes: Optional[str] = None
    ) -> BookLoss:
        """Confirm a book loss"""
        result = await self.db.execute(
            select(BookLoss).where(BookLoss.id == loss_id)
        )
        book_loss = result.scalar_one_or_none()
        
        if not book_loss:
            raise ValueError(f"Book loss {loss_id} not found")
        
        book_loss.status = LossStatus.CONFIRMED
        book_loss.resolved_by = confirmed_by
        book_loss.resolution_notes = resolution_notes
        
        await self.db.commit()
        await self.db.refresh(book_loss)
        
        logger.info(f"Book loss {loss_id} confirmed")
        
        return book_loss
    
    async def record_payment(
        self,
        loss_id: int,
        amount: float
    ) -> BookLoss:
        """Record payment for lost book"""
        result = await self.db.execute(
            select(BookLoss).where(BookLoss.id == loss_id)
        )
        book_loss = result.scalar_one_or_none()
        
        if not book_loss:
            raise ValueError(f"Book loss {loss_id} not found")
        
        book_loss.amount_paid += amount
        
        if book_loss.amount_paid >= book_loss.total_fine:
            book_loss.is_paid = True
            book_loss.paid_date = datetime.utcnow()
            book_loss.status = LossStatus.RESOLVED
        
        await self.db.commit()
        await self.db.refresh(book_loss)
        
        logger.info(f"Recorded payment of ₹{amount} for book loss {loss_id}")
        
        return book_loss
    
    async def waive_loss(
        self,
        loss_id: int,
        reason: str,
        waived_by: int
    ) -> BookLoss:
        """Waive a book loss"""
        result = await self.db.execute(
            select(BookLoss).where(BookLoss.id == loss_id)
        )
        book_loss = result.scalar_one_or_none()
        
        if not book_loss:
            raise ValueError(f"Book loss {loss_id} not found")
        
        book_loss.status = LossStatus.WAIVED
        book_loss.resolution_notes = f"Waived by {waived_by}: {reason}"
        book_loss.is_paid = True
        book_loss.paid_date = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(book_loss)
        
        logger.info(f"Book loss {loss_id} waived")
        
        return book_loss
    
    async def get_losses_by_member(
        self,
        member_id: int,
        status: Optional[LossStatus] = None
    ) -> List[BookLoss]:
        """Get all book losses for a member"""
        query = select(BookLoss).where(BookLoss.member_id == member_id)
        
        if status:
            query = query.where(BookLoss.status == status)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_unpaid_losses(self) -> List[BookLoss]:
        """Get all unpaid book losses"""
        result = await self.db.execute(
            select(BookLoss).where(
                and_(
                    BookLoss.is_paid == False,
                    BookLoss.status.in_([LossStatus.CONFIRMED, LossStatus.REPORTED])
                )
            )
        )
        return result.scalars().all()
    
    async def update_lost_book_settings(
        self,
        processing_fine_percentage: Optional[float] = None,
        minimum_processing_fine: Optional[float] = None,
        maximum_processing_fine: Optional[float] = None,
        grace_period_days: Optional[int] = None
    ) -> LostBookSettings:
        """Update lost book settings"""
        settings = await self.get_lost_book_settings()
        
        if not settings:
            settings = LostBookSettings()
            self.db.add(settings)
        
        if processing_fine_percentage is not None:
            settings.processing_fine_percentage = processing_fine_percentage
        if minimum_processing_fine is not None:
            settings.minimum_processing_fine = minimum_processing_fine
        if maximum_processing_fine is not None:
            settings.maximum_processing_fine = maximum_processing_fine
        if grace_period_days is not None:
            settings.grace_period_days = grace_period_days
        
        await self.db.commit()
        await self.db.refresh(settings)
        
        logger.info("Updated lost book settings")
        
        return settings
