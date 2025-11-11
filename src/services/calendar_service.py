"""Academic Calendar Service for EMIS"""
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, extract
from uuid import UUID

from src.models.academic_calendar import (
    AcademicCalendar, Holiday, ImportantDate, CalendarSubscription,
    CalendarEventType, CalendarEventStatus
)
from src.lib.logging import get_logger

logger = get_logger(__name__)


class CalendarService:
    """Service for managing academic calendar"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # ==================== EVENT MANAGEMENT ====================
    
    async def create_event(
        self,
        title: str,
        event_type: CalendarEventType,
        start_date: date,
        created_by: int,
        **kwargs
    ) -> AcademicCalendar:
        """Create a calendar event"""
        
        event = AcademicCalendar(
            title=title,
            event_type=event_type,
            start_date=start_date,
            created_by=created_by,
            **kwargs
        )
        
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        
        logger.info(f"Created calendar event: {title} on {start_date}")
        
        return event
    
    async def add_examination_to_calendar(
        self,
        exam_id: int,
        exam_title: str,
        exam_date: date,
        end_date: Optional[date],
        created_by: int,
        **kwargs
    ) -> AcademicCalendar:
        """Quick method to add examination to calendar"""
        
        return await self.create_event(
            title=f"Examination: {exam_title}",
            event_type=CalendarEventType.EXAMINATION,
            start_date=exam_date,
            end_date=end_date,
            exam_id=exam_id,
            created_by=created_by,
            color_code="#FF5733",
            icon="exam",
            priority=2,  # High priority
            **kwargs
        )
    
    async def add_program_event(
        self,
        program_id: int,
        title: str,
        event_date: date,
        created_by: int,
        **kwargs
    ) -> AcademicCalendar:
        """Quick method to add program event to calendar"""
        
        return await self.create_event(
            title=title,
            event_type=CalendarEventType.PROGRAM_EVENT,
            start_date=event_date,
            program_id=program_id,
            created_by=created_by,
            color_code="#3498DB",
            icon="program",
            **kwargs
        )
    
    async def add_holiday(
        self,
        name: str,
        holiday_date: date,
        created_by: int,
        holiday_type: str = "college",
        **kwargs
    ) -> Holiday:
        """Quick method to add holiday"""
        
        # Create holiday record
        holiday = Holiday(
            name=name,
            holiday_date=holiday_date,
            holiday_type=holiday_type,
            created_by=created_by,
            **kwargs
        )
        
        self.db.add(holiday)
        
        # Also create calendar event
        calendar_event = AcademicCalendar(
            title=f"Holiday: {name}",
            event_type=CalendarEventType.HOLIDAY,
            start_date=holiday_date,
            created_by=created_by,
            color_code="#E74C3C",
            icon="holiday",
            is_all_day=True,
            status=CalendarEventStatus.SCHEDULED
        )
        
        self.db.add(calendar_event)
        await self.db.commit()
        
        # Link them
        holiday.calendar_event_id = calendar_event.id
        await self.db.commit()
        await self.db.refresh(holiday)
        
        logger.info(f"Added holiday: {name} on {holiday_date}")
        
        return holiday
    
    async def add_deadline(
        self,
        title: str,
        deadline_date: date,
        category: str,
        created_by: int,
        **kwargs
    ) -> ImportantDate:
        """Quick method to add important deadline"""
        
        deadline = ImportantDate(
            title=title,
            deadline_date=deadline_date,
            category=category,
            created_by=created_by,
            **kwargs
        )
        
        self.db.add(deadline)
        
        # Also create calendar event
        calendar_event = AcademicCalendar(
            title=f"Deadline: {title}",
            event_type=CalendarEventType.DEADLINE,
            start_date=deadline_date,
            created_by=created_by,
            color_code="#F39C12",
            icon="deadline",
            priority=1,
            **kwargs
        )
        
        self.db.add(calendar_event)
        await self.db.commit()
        
        deadline.calendar_event_id = calendar_event.id
        await self.db.commit()
        await self.db.refresh(deadline)
        
        logger.info(f"Added deadline: {title} on {deadline_date}")
        
        return deadline
    
    async def bulk_add_holidays(
        self,
        holidays: List[Dict],
        created_by: int
    ) -> List[Holiday]:
        """Bulk add holidays (useful for yearly calendar setup)"""
        
        holiday_list = []
        
        for h in holidays:
            holiday = await self.add_holiday(
                name=h['name'],
                holiday_date=h['date'],
                created_by=created_by,
                holiday_type=h.get('type', 'college'),
                academic_year=h.get('academic_year'),
                description=h.get('description')
            )
            holiday_list.append(holiday)
        
        logger.info(f"Bulk added {len(holiday_list)} holidays")
        
        return holiday_list
    
    # ==================== CALENDAR RETRIEVAL ====================
    
    async def get_calendar(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        event_types: Optional[List[str]] = None,
        academic_year: Optional[str] = None,
        semester: Optional[int] = None,
        program_id: Optional[int] = None,
        is_published: bool = True
    ) -> List[AcademicCalendar]:
        """Get calendar events with filters"""
        
        query = select(AcademicCalendar)
        
        conditions = []
        
        if is_published:
            conditions.append(AcademicCalendar.is_published == True)
        
        if start_date:
            conditions.append(AcademicCalendar.start_date >= start_date)
        
        if end_date:
            conditions.append(
                or_(
                    AcademicCalendar.end_date <= end_date,
                    and_(
                        AcademicCalendar.end_date.is_(None),
                        AcademicCalendar.start_date <= end_date
                    )
                )
            )
        
        if event_types:
            conditions.append(AcademicCalendar.event_type.in_(event_types))
        
        if academic_year:
            conditions.append(AcademicCalendar.academic_year == academic_year)
        
        if semester:
            conditions.append(AcademicCalendar.semester == semester)
        
        if program_id:
            conditions.append(
                or_(
                    AcademicCalendar.program_id == program_id,
                    AcademicCalendar.program_id.is_(None)  # Include general events
                )
            )
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.order_by(AcademicCalendar.start_date.asc())
        
        result = await self.db.execute(query)
        events = result.scalars().all()
        
        logger.info(f"Retrieved {len(events)} calendar events")
        
        return events
    
    async def get_month_calendar(
        self,
        year: int,
        month: int,
        **kwargs
    ) -> List[AcademicCalendar]:
        """Get calendar for a specific month"""
        
        start_date = date(year, month, 1)
        
        # Get last day of month
        if month == 12:
            end_date = date(year, 12, 31)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        return await self.get_calendar(
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )
    
    async def get_week_calendar(
        self,
        start_date: date,
        **kwargs
    ) -> List[AcademicCalendar]:
        """Get calendar for a week starting from given date"""
        
        end_date = start_date + timedelta(days=6)
        
        return await self.get_calendar(
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )
    
    async def get_today_events(self, **kwargs) -> List[AcademicCalendar]:
        """Get today's events"""
        
        today = date.today()
        
        return await self.get_calendar(
            start_date=today,
            end_date=today,
            **kwargs
        )
    
    async def get_upcoming_events(
        self,
        days: int = 7,
        **kwargs
    ) -> List[AcademicCalendar]:
        """Get upcoming events for next N days"""
        
        start_date = date.today()
        end_date = start_date + timedelta(days=days)
        
        return await self.get_calendar(
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )
    
    async def get_holidays(
        self,
        academic_year: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Holiday]:
        """Get holidays"""
        
        query = select(Holiday)
        
        conditions = []
        
        if academic_year:
            conditions.append(Holiday.academic_year == academic_year)
        
        if start_date:
            conditions.append(Holiday.holiday_date >= start_date)
        
        if end_date:
            conditions.append(Holiday.holiday_date <= end_date)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.order_by(Holiday.holiday_date.asc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_deadlines(
        self,
        category: Optional[str] = None,
        academic_year: Optional[str] = None,
        is_active: bool = True
    ) -> List[ImportantDate]:
        """Get important deadlines"""
        
        query = select(ImportantDate)
        
        conditions = [ImportantDate.is_active == is_active]
        
        if category:
            conditions.append(ImportantDate.category == category)
        
        if academic_year:
            conditions.append(ImportantDate.academic_year == academic_year)
        
        # Only future/current deadlines
        conditions.append(ImportantDate.deadline_date >= date.today())
        
        query = query.where(and_(*conditions))
        query = query.order_by(ImportantDate.deadline_date.asc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    # ==================== EVENT UPDATES ====================
    
    async def publish_event(
        self,
        event_id: UUID,
        published_by: int
    ) -> AcademicCalendar:
        """Publish calendar event"""
        
        result = await self.db.execute(
            select(AcademicCalendar).where(AcademicCalendar.id == event_id)
        )
        event = result.scalar_one_or_none()
        
        if not event:
            raise ValueError(f"Event {event_id} not found")
        
        event.is_published = True
        event.published_by = published_by
        event.published_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(event)
        
        logger.info(f"Published event: {event.title}")
        
        return event
    
    async def cancel_event(
        self,
        event_id: UUID,
        cancelled_by: int,
        reason: str
    ) -> AcademicCalendar:
        """Cancel calendar event"""
        
        result = await self.db.execute(
            select(AcademicCalendar).where(AcademicCalendar.id == event_id)
        )
        event = result.scalar_one_or_none()
        
        if not event:
            raise ValueError(f"Event {event_id} not found")
        
        event.status = CalendarEventStatus.CANCELLED
        event.cancelled_by = cancelled_by
        event.cancelled_at = datetime.utcnow()
        event.cancellation_reason = reason
        
        await self.db.commit()
        await self.db.refresh(event)
        
        logger.info(f"Cancelled event: {event.title}")
        
        return event
    
    async def postpone_event(
        self,
        event_id: UUID,
        new_date: date,
        updated_by: int
    ) -> AcademicCalendar:
        """Postpone calendar event"""
        
        result = await self.db.execute(
            select(AcademicCalendar).where(AcademicCalendar.id == event_id)
        )
        event = result.scalar_one_or_none()
        
        if not event:
            raise ValueError(f"Event {event_id} not found")
        
        event.status = CalendarEventStatus.POSTPONED
        event.postponed_to_date = new_date
        event.updated_by = updated_by
        event.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(event)
        
        logger.info(f"Postponed event: {event.title} to {new_date}")
        
        return event
    
    # ==================== STATISTICS ====================
    
    async def get_calendar_summary(
        self,
        academic_year: str,
        semester: Optional[int] = None
    ) -> Dict:
        """Get calendar summary statistics"""
        
        query = select(AcademicCalendar).where(
            AcademicCalendar.academic_year == academic_year
        )
        
        if semester:
            query = query.where(AcademicCalendar.semester == semester)
        
        result = await self.db.execute(query)
        events = result.scalars().all()
        
        # Count by type
        type_counts = {}
        for event in events:
            type_counts[event.event_type] = type_counts.get(event.event_type, 0) + 1
        
        # Count by status
        status_counts = {}
        for event in events:
            status_counts[event.status] = status_counts.get(event.status, 0) + 1
        
        # Get holidays count
        holidays_result = await self.db.execute(
            select(func.count(Holiday.id)).where(
                Holiday.academic_year == academic_year
            )
        )
        holidays_count = holidays_result.scalar()
        
        summary = {
            'total_events': len(events),
            'by_type': type_counts,
            'by_status': status_counts,
            'total_holidays': holidays_count,
            'upcoming_events': len([e for e in events if e.is_upcoming]),
            'past_events': len([e for e in events if e.is_past])
        }
        
        return summary
