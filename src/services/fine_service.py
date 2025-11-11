"""Fine Service for managing library fines with configurable settings"""
from typing import List, Optional
from datetime import datetime, date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.library_settings import LibrarySettings, MemberType, FineWaiver
from src.lib.audit import audit_log


class FineService:
    """Service for managing library fines"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_library_settings(self, member_type: MemberType) -> Optional[LibrarySettings]:
        """Get library settings for a member type"""
        result = await self.db.execute(
            select(LibrarySettings).where(
                LibrarySettings.member_type == member_type,
                LibrarySettings.is_active == True
            )
        )
        return result.scalar_one_or_none()
    
    async def get_all_library_settings(self) -> List[LibrarySettings]:
        """Get all active library settings"""
        result = await self.db.execute(
            select(LibrarySettings).where(LibrarySettings.is_active == True)
        )
        return list(result.scalars().all())
    
    async def create_library_settings(
        self,
        member_type: MemberType,
        max_books_allowed: int = 3,
        borrowing_period_days: int = 14,
        fine_per_day: float = 5.0,
        grace_period_days: int = 0,
        max_fine_amount: float = 500.0,
        max_reservations: int = 2,
        reservation_hold_days: int = 3,
        max_renewals: int = 2,
        digital_access_enabled: bool = True,
        digital_download_limit: int = 10,
        description: Optional[str] = None,
        updated_by: Optional[int] = None
    ) -> LibrarySettings:
        """Create or update library settings for a member type"""
        existing = await self.get_library_settings(member_type)
        
        if existing:
            existing.max_books_allowed = max_books_allowed
            existing.borrowing_period_days = borrowing_period_days
            existing.fine_per_day = fine_per_day
            existing.grace_period_days = grace_period_days
            existing.max_fine_amount = max_fine_amount
            existing.max_reservations = max_reservations
            existing.reservation_hold_days = reservation_hold_days
            existing.max_renewals = max_renewals
            existing.digital_access_enabled = digital_access_enabled
            existing.digital_download_limit = digital_download_limit
            existing.description = description
            existing.updated_by = updated_by
            existing.updated_at = datetime.utcnow()
            
            await self.db.commit()
            await self.db.refresh(existing)
            return existing
        
        settings = LibrarySettings(
            member_type=member_type,
            max_books_allowed=max_books_allowed,
            borrowing_period_days=borrowing_period_days,
            fine_per_day=fine_per_day,
            grace_period_days=grace_period_days,
            max_fine_amount=max_fine_amount,
            max_reservations=max_reservations,
            reservation_hold_days=reservation_hold_days,
            max_renewals=max_renewals,
            digital_access_enabled=digital_access_enabled,
            digital_download_limit=digital_download_limit,
            description=description,
            updated_by=updated_by
        )
        
        self.db.add(settings)
        await self.db.commit()
        await self.db.refresh(settings)
        
        await audit_log(
            self.db,
            action="create_library_settings",
            entity_type="library_settings",
            entity_id=settings.id,
            user_id=updated_by,
            details={"member_type": member_type.value}
        )
        
        return settings
    
    async def calculate_fine(
        self,
        member_type: MemberType,
        due_date: date,
        return_date: Optional[date] = None
    ) -> tuple[float, int]:
        """
        Calculate fine amount for an overdue book
        Returns: (fine_amount, days_overdue)
        """
        settings = await self.get_library_settings(member_type)
        if not settings:
            # Default settings if not configured
            fine_per_day = 5.0
            grace_period = 0
            max_fine = 500.0
        else:
            fine_per_day = settings.fine_per_day
            grace_period = settings.grace_period_days
            max_fine = settings.max_fine_amount
        
        actual_return_date = return_date or date.today()
        days_overdue = (actual_return_date - due_date).days
        
        if days_overdue <= grace_period:
            return 0.0, days_overdue
        
        chargeable_days = days_overdue - grace_period
        fine_amount = chargeable_days * fine_per_day
        
        fine_amount = min(fine_amount, max_fine)
        
        return round(fine_amount, 2), days_overdue
    
    async def create_fine_waiver(
        self,
        fine_id: int,
        member_id: int,
        original_amount: float,
        waived_amount: float,
        reason: str,
        approved_by: int
    ) -> FineWaiver:
        """Create a fine waiver"""
        final_amount = max(0, original_amount - waived_amount)
        
        waiver = FineWaiver(
            fine_id=fine_id,
            member_id=member_id,
            original_amount=original_amount,
            waived_amount=waived_amount,
            final_amount=final_amount,
            reason=reason,
            approved_by=approved_by
        )
        
        self.db.add(waiver)
        await self.db.commit()
        await self.db.refresh(waiver)
        
        await audit_log(
            self.db,
            action="create_fine_waiver",
            entity_type="fine_waiver",
            entity_id=waiver.id,
            user_id=approved_by,
            details={
                "fine_id": fine_id,
                "original_amount": original_amount,
                "waived_amount": waived_amount,
                "final_amount": final_amount
            }
        )
        
        return waiver
    
    async def get_fine_waivers_by_member(self, member_id: int) -> List[FineWaiver]:
        """Get all fine waivers for a member"""
        result = await self.db.execute(
            select(FineWaiver).where(FineWaiver.member_id == member_id)
        )
        return list(result.scalars().all())
    
    async def update_library_settings(
        self,
        settings_id: int,
        updates: dict,
        updated_by: Optional[int] = None
    ) -> Optional[LibrarySettings]:
        """Update library settings"""
        result = await self.db.execute(
            select(LibrarySettings).where(LibrarySettings.id == settings_id)
        )
        settings = result.scalar_one_or_none()
        
        if not settings:
            return None
        
        for key, value in updates.items():
            if hasattr(settings, key) and key not in ['id', 'member_type', 'created_at']:
                setattr(settings, key, value)
        
        settings.updated_by = updated_by
        settings.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(settings)
        
        await audit_log(
            self.db,
            action="update_library_settings",
            entity_type="library_settings",
            entity_id=settings_id,
            user_id=updated_by,
            details=updates
        )
        
        return settings
    
    async def initialize_default_settings(self, created_by: Optional[int] = None):
        """Initialize default library settings for all member types"""
        default_settings = {
            MemberType.STUDENT: {
                "max_books_allowed": 3,
                "borrowing_period_days": 14,
                "fine_per_day": 5.0,
                "grace_period_days": 0,
                "max_fine_amount": 500.0,
                "max_reservations": 2,
                "description": "Default settings for students"
            },
            MemberType.FACULTY: {
                "max_books_allowed": 10,
                "borrowing_period_days": 30,
                "fine_per_day": 10.0,
                "grace_period_days": 2,
                "max_fine_amount": 1000.0,
                "max_reservations": 5,
                "description": "Default settings for faculty"
            },
            MemberType.STAFF: {
                "max_books_allowed": 5,
                "borrowing_period_days": 21,
                "fine_per_day": 5.0,
                "grace_period_days": 1,
                "max_fine_amount": 500.0,
                "max_reservations": 3,
                "description": "Default settings for staff"
            },
            MemberType.ALUMNI: {
                "max_books_allowed": 2,
                "borrowing_period_days": 14,
                "fine_per_day": 10.0,
                "grace_period_days": 0,
                "max_fine_amount": 500.0,
                "max_reservations": 1,
                "description": "Default settings for alumni"
            },
            MemberType.GUEST: {
                "max_books_allowed": 1,
                "borrowing_period_days": 7,
                "fine_per_day": 15.0,
                "grace_period_days": 0,
                "max_fine_amount": 300.0,
                "max_reservations": 0,
                "description": "Default settings for guests"
            }
        }
        
        for member_type, config in default_settings.items():
            await self.create_library_settings(
                member_type=member_type,
                updated_by=created_by,
                **config
            )
