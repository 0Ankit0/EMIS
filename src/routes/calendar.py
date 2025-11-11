"""Academic Calendar API Endpoints"""
from datetime import date, datetime, time
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.database import get_db
from src.middleware.rbac import require_permissions
from src.services.calendar_service import CalendarService
from src.models.academic_calendar import CalendarEventType, CalendarEventStatus

router = APIRouter(prefix="/api/calendar", tags=["Academic Calendar"])


# ==================== REQUEST MODELS ====================

class CalendarEventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    event_type: str
    start_date: date
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_all_day: bool = True
    academic_year: Optional[str] = None
    semester: Optional[int] = None
    program_id: Optional[int] = None
    location: Optional[str] = None
    venue: Optional[str] = None
    organizer: Optional[str] = None
    color_code: Optional[str] = None
    priority: Optional[int] = 0
    is_for_students: bool = True
    is_for_faculty: bool = True
    is_for_staff: bool = False


class ExaminationEventCreate(BaseModel):
    exam_id: int
    exam_title: str
    exam_date: date
    end_date: Optional[date] = None
    academic_year: str
    semester: int
    venue: Optional[str] = None
    description: Optional[str] = None


class ProgramEventCreate(BaseModel):
    program_id: int
    title: str
    event_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None
    location: Optional[str] = None


class HolidayCreate(BaseModel):
    name: str
    holiday_date: date
    holiday_type: str = "college"
    description: Optional[str] = None
    academic_year: Optional[str] = None
    is_restricted: bool = False


class BulkHolidayCreate(BaseModel):
    holidays: List[dict]


class DeadlineCreate(BaseModel):
    title: str
    deadline_date: date
    deadline_time: Optional[time] = None
    category: str
    description: Optional[str] = None
    academic_year: Optional[str] = None
    semester: Optional[int] = None


class EventPublish(BaseModel):
    event_ids: List[UUID]


class EventCancel(BaseModel):
    reason: str


class EventPostpone(BaseModel):
    new_date: date


# ==================== ENDPOINTS ====================

@router.post("/events", status_code=status.HTTP_201_CREATED)
async def create_calendar_event(
    event_data: CalendarEventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:create"]))
):
    """Create a general calendar event"""
    service = CalendarService(db)
    
    event = await service.create_event(
        **event_data.dict(),
        created_by=current_user.get("id")
    )
    
    return {
        "id": event.id,
        "title": event.title,
        "event_type": event.event_type,
        "start_date": event.start_date,
        "status": event.status,
        "message": "Calendar event created successfully"
    }


@router.post("/events/examination", status_code=status.HTTP_201_CREATED)
async def add_examination_to_calendar(
    exam_data: ExaminationEventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:create"]))
):
    """Quick add examination to calendar"""
    service = CalendarService(db)
    
    event = await service.add_examination_to_calendar(
        **exam_data.dict(),
        created_by=current_user.get("id")
    )
    
    return {
        "id": event.id,
        "title": event.title,
        "exam_id": event.exam_id,
        "start_date": event.start_date,
        "message": "Examination added to calendar"
    }


@router.post("/events/program", status_code=status.HTTP_201_CREATED)
async def add_program_event(
    program_data: ProgramEventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:create"]))
):
    """Quick add program event to calendar"""
    service = CalendarService(db)
    
    event = await service.add_program_event(
        **program_data.dict(),
        created_by=current_user.get("id")
    )
    
    return {
        "id": event.id,
        "title": event.title,
        "program_id": event.program_id,
        "start_date": event.start_date,
        "message": "Program event added to calendar"
    }


@router.post("/holidays", status_code=status.HTTP_201_CREATED)
async def add_holiday(
    holiday_data: HolidayCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:create"]))
):
    """Add holiday to calendar"""
    service = CalendarService(db)
    
    holiday = await service.add_holiday(
        **holiday_data.dict(),
        created_by=current_user.get("id")
    )
    
    return {
        "id": holiday.id,
        "name": holiday.name,
        "holiday_date": holiday.holiday_date,
        "holiday_type": holiday.holiday_type,
        "message": "Holiday added to calendar"
    }


@router.post("/holidays/bulk", status_code=status.HTTP_201_CREATED)
async def bulk_add_holidays(
    bulk_data: BulkHolidayCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:create"]))
):
    """Bulk add holidays (e.g., yearly calendar setup)"""
    service = CalendarService(db)
    
    holidays = await service.bulk_add_holidays(
        holidays=bulk_data.holidays,
        created_by=current_user.get("id")
    )
    
    return {
        "total_added": len(holidays),
        "holidays": [
            {
                "name": h.name,
                "date": h.holiday_date,
                "type": h.holiday_type
            }
            for h in holidays
        ],
        "message": f"Successfully added {len(holidays)} holidays"
    }


@router.post("/deadlines", status_code=status.HTTP_201_CREATED)
async def add_deadline(
    deadline_data: DeadlineCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:create"]))
):
    """Add important deadline to calendar"""
    service = CalendarService(db)
    
    deadline = await service.add_deadline(
        **deadline_data.dict(),
        created_by=current_user.get("id")
    )
    
    return {
        "id": deadline.id,
        "title": deadline.title,
        "deadline_date": deadline.deadline_date,
        "category": deadline.category,
        "message": "Deadline added to calendar"
    }


@router.get("/")
async def get_calendar(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    event_types: Optional[List[str]] = Query(None),
    academic_year: Optional[str] = Query(None),
    semester: Optional[int] = Query(None),
    program_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:read"]))
):
    """
    Get calendar events with filters
    
    Use this endpoint to display the calendar in your UI
    """
    service = CalendarService(db)
    
    events = await service.get_calendar(
        start_date=start_date,
        end_date=end_date,
        event_types=event_types,
        academic_year=academic_year,
        semester=semester,
        program_id=program_id
    )
    
    return {
        "total": len(events),
        "events": [
            {
                "id": e.id,
                "title": e.title,
                "description": e.description,
                "event_type": e.event_type,
                "start_date": e.start_date,
                "end_date": e.end_date,
                "start_time": e.start_time,
                "end_time": e.end_time,
                "is_all_day": e.is_all_day,
                "location": e.location,
                "venue": e.venue,
                "status": e.status,
                "color_code": e.color_code,
                "icon": e.icon,
                "priority": e.priority,
                "is_upcoming": e.is_upcoming,
                "is_today": e.is_today,
                "duration_days": e.duration_days
            }
            for e in events
        ]
    }


@router.get("/month/{year}/{month}")
async def get_month_calendar(
    year: int,
    month: int,
    academic_year: Optional[str] = Query(None),
    program_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:read"]))
):
    """Get calendar for a specific month"""
    service = CalendarService(db)
    
    events = await service.get_month_calendar(
        year=year,
        month=month,
        academic_year=academic_year,
        program_id=program_id
    )
    
    return {
        "year": year,
        "month": month,
        "total": len(events),
        "events": [
            {
                "id": e.id,
                "title": e.title,
                "event_type": e.event_type,
                "start_date": e.start_date,
                "end_date": e.end_date,
                "color_code": e.color_code,
                "status": e.status
            }
            for e in events
        ]
    }


@router.get("/today")
async def get_today_events(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:read"]))
):
    """Get today's events"""
    service = CalendarService(db)
    
    events = await service.get_today_events()
    
    return {
        "date": date.today(),
        "total": len(events),
        "events": [
            {
                "id": e.id,
                "title": e.title,
                "event_type": e.event_type,
                "start_time": e.start_time,
                "end_time": e.end_time,
                "location": e.location,
                "color_code": e.color_code
            }
            for e in events
        ]
    }


@router.get("/upcoming")
async def get_upcoming_events(
    days: int = Query(7, ge=1, le=90),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:read"]))
):
    """Get upcoming events for next N days"""
    service = CalendarService(db)
    
    events = await service.get_upcoming_events(days=days)
    
    return {
        "days": days,
        "total": len(events),
        "events": [
            {
                "id": e.id,
                "title": e.title,
                "event_type": e.event_type,
                "start_date": e.start_date,
                "location": e.location,
                "priority": e.priority,
                "color_code": e.color_code
            }
            for e in events
        ]
    }


@router.get("/holidays")
async def get_holidays(
    academic_year: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:read"]))
):
    """Get holidays"""
    service = CalendarService(db)
    
    holidays = await service.get_holidays(
        academic_year=academic_year,
        start_date=start_date,
        end_date=end_date
    )
    
    return {
        "total": len(holidays),
        "holidays": [
            {
                "id": h.id,
                "name": h.name,
                "holiday_date": h.holiday_date,
                "holiday_type": h.holiday_type,
                "description": h.description,
                "is_restricted": h.is_restricted
            }
            for h in holidays
        ]
    }


@router.get("/deadlines")
async def get_deadlines(
    category: Optional[str] = Query(None),
    academic_year: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:read"]))
):
    """Get important deadlines"""
    service = CalendarService(db)
    
    deadlines = await service.get_deadlines(
        category=category,
        academic_year=academic_year
    )
    
    return {
        "total": len(deadlines),
        "deadlines": [
            {
                "id": d.id,
                "title": d.title,
                "deadline_date": d.deadline_date,
                "deadline_time": d.deadline_time,
                "category": d.category,
                "description": d.description
            }
            for d in deadlines
        ]
    }


@router.post("/events/{event_id}/publish")
async def publish_event(
    event_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:publish"]))
):
    """Publish calendar event to make it visible to users"""
    service = CalendarService(db)
    
    try:
        event = await service.publish_event(
            event_id=event_id,
            published_by=current_user.get("id")
        )
        
        return {
            "id": event.id,
            "title": event.title,
            "is_published": event.is_published,
            "published_at": event.published_at,
            "message": "Event published successfully"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/events/{event_id}/cancel")
async def cancel_event(
    event_id: UUID,
    cancel_data: EventCancel,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:update"]))
):
    """Cancel calendar event"""
    service = CalendarService(db)
    
    try:
        event = await service.cancel_event(
            event_id=event_id,
            cancelled_by=current_user.get("id"),
            reason=cancel_data.reason
        )
        
        return {
            "id": event.id,
            "title": event.title,
            "status": event.status,
            "cancelled_at": event.cancelled_at,
            "message": "Event cancelled successfully"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/events/{event_id}/postpone")
async def postpone_event(
    event_id: UUID,
    postpone_data: EventPostpone,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:update"]))
):
    """Postpone calendar event to new date"""
    service = CalendarService(db)
    
    try:
        event = await service.postpone_event(
            event_id=event_id,
            new_date=postpone_data.new_date,
            updated_by=current_user.get("id")
        )
        
        return {
            "id": event.id,
            "title": event.title,
            "status": event.status,
            "original_date": event.start_date,
            "postponed_to": event.postponed_to_date,
            "message": "Event postponed successfully"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/summary")
async def get_calendar_summary(
    academic_year: str,
    semester: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["calendar:read"]))
):
    """Get calendar summary statistics"""
    service = CalendarService(db)
    
    summary = await service.get_calendar_summary(
        academic_year=academic_year,
        semester=semester
    )
    
    return summary
