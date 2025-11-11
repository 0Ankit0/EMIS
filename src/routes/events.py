"""
Event Management API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from src.database import get_db
from src.services.event_service import EventService
from src.models.event import EventType, EventStatus, RegistrationStatus
from src.middleware.rbac import get_current_user
from src.models.auth import User

router = APIRouter(prefix="/api/events", tags=["Events"])


# Pydantic Models
class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    event_type: EventType
    start_date: datetime
    end_date: datetime
    registration_start: Optional[datetime] = None
    registration_end: Optional[datetime] = None
    venue: Optional[str] = None
    venue_details: Optional[str] = None
    max_participants: Optional[int] = None
    registration_fee: Optional[float] = 0
    is_paid_event: bool = False
    department_id: Optional[int] = None
    coordinator_name: Optional[str] = None
    coordinator_contact: Optional[str] = None
    coordinator_email: Optional[str] = None
    is_inter_college: bool = False
    requires_approval: bool = True


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[EventStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_participants: Optional[int] = None
    is_published: Optional[bool] = None


class EventRegistrationCreate(BaseModel):
    participant_name: str
    participant_email: str
    participant_phone: Optional[str] = None
    college_name: Optional[str] = None
    team_name: Optional[str] = None
    team_members: Optional[str] = None
    remarks: Optional[str] = None


class BudgetCreate(BaseModel):
    category: str
    description: Optional[str] = None
    estimated_amount: float


class BudgetApproval(BaseModel):
    approved_amount: float


class AttendanceCreate(BaseModel):
    participant_name: str
    check_in_time: Optional[datetime] = None
    attendance_date: Optional[datetime] = None
    session_name: Optional[str] = None


# Event Endpoints
@router.post("/", response_model=dict)
def create_event(
    event_data: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new event"""
    service = EventService(db)
    event = service.create_event(event_data.dict(), current_user.id)
    return {"message": "Event created successfully", "event_id": event.id}


@router.get("/", response_model=List[dict])
def get_events(
    event_type: Optional[EventType] = None,
    status: Optional[EventStatus] = None,
    department_id: Optional[int] = None,
    is_published: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all events"""
    service = EventService(db)
    events = service.get_events(
        event_type=event_type,
        status=status,
        department_id=department_id,
        is_published=is_published,
        skip=skip,
        limit=limit
    )
    return [
        {
            "id": e.id,
            "title": e.title,
            "event_type": e.event_type,
            "status": e.status,
            "start_date": e.start_date,
            "end_date": e.end_date,
            "venue": e.venue,
            "max_participants": e.max_participants,
            "current_participants": e.current_participants,
            "is_published": e.is_published
        }
        for e in events
    ]


@router.get("/{event_id}", response_model=dict)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get event details"""
    service = EventService(db)
    event = service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "event_type": event.event_type,
        "status": event.status,
        "start_date": event.start_date,
        "end_date": event.end_date,
        "registration_start": event.registration_start,
        "registration_end": event.registration_end,
        "venue": event.venue,
        "max_participants": event.max_participants,
        "current_participants": event.current_participants,
        "registration_fee": float(event.registration_fee) if event.registration_fee else 0,
        "is_paid_event": event.is_paid_event,
        "coordinator_name": event.coordinator_name,
        "coordinator_contact": event.coordinator_contact,
        "is_published": event.is_published
    }


@router.put("/{event_id}", response_model=dict)
def update_event(
    event_id: int,
    event_data: EventUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update event"""
    service = EventService(db)
    event = service.update_event(event_id, event_data.dict(exclude_unset=True))
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event updated successfully"}


@router.delete("/{event_id}", response_model=dict)
def delete_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete event"""
    service = EventService(db)
    success = service.delete_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted successfully"}


# Registration Endpoints
@router.post("/{event_id}/register", response_model=dict)
def register_for_event(
    event_id: int,
    registration_data: EventRegistrationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register for an event"""
    service = EventService(db)
    try:
        registration = service.register_for_event(
            event_id,
            registration_data.dict(),
            user_id=current_user.id
        )
        return {
            "message": "Registration successful",
            "registration_id": registration.id,
            "status": registration.status
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{event_id}/registrations", response_model=List[dict])
def get_event_registrations(
    event_id: int,
    status: Optional[RegistrationStatus] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get registrations for an event"""
    service = EventService(db)
    registrations = service.get_event_registrations(event_id, status)
    return [
        {
            "id": r.id,
            "participant_name": r.participant_name,
            "participant_email": r.participant_email,
            "status": r.status,
            "registration_date": r.registration_date,
            "team_name": r.team_name
        }
        for r in registrations
    ]


@router.post("/registrations/{registration_id}/approve", response_model=dict)
def approve_registration(
    registration_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Approve event registration"""
    service = EventService(db)
    try:
        registration = service.approve_registration(registration_id, current_user.id)
        return {"message": "Registration approved", "registration_id": registration.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/registrations/{registration_id}/reject", response_model=dict)
def reject_registration(
    registration_id: int,
    reason: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reject event registration"""
    service = EventService(db)
    try:
        registration = service.reject_registration(registration_id, reason)
        return {"message": "Registration rejected", "registration_id": registration.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Budget Endpoints
@router.post("/{event_id}/budget", response_model=dict)
def add_budget_item(
    event_id: int,
    budget_data: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add budget item to event"""
    service = EventService(db)
    budget = service.add_budget_item(event_id, budget_data.dict())
    return {"message": "Budget item added", "budget_id": budget.id}


@router.post("/budget/{budget_id}/approve", response_model=dict)
def approve_budget(
    budget_id: int,
    approval_data: BudgetApproval,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Approve budget item"""
    service = EventService(db)
    budget = service.approve_budget(budget_id, current_user.id, approval_data.approved_amount)
    return {"message": "Budget approved", "budget_id": budget.id}


@router.get("/{event_id}/budget/summary", response_model=dict)
def get_budget_summary(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get budget summary for event"""
    service = EventService(db)
    return service.get_event_budget_summary(event_id)


# Attendance Endpoints
@router.post("/{event_id}/attendance/{registration_id}", response_model=dict)
def mark_attendance(
    event_id: int,
    registration_id: int,
    attendance_data: AttendanceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark attendance for event"""
    service = EventService(db)
    attendance = service.mark_attendance(event_id, registration_id, attendance_data.dict())
    return {"message": "Attendance marked", "attendance_id": attendance.id}


@router.get("/{event_id}/attendance/report", response_model=dict)
def get_attendance_report(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get attendance report for event"""
    service = EventService(db)
    return service.get_attendance_report(event_id)


# Statistics
@router.get("/{event_id}/statistics", response_model=dict)
def get_event_statistics(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive statistics for event"""
    service = EventService(db)
    return service.get_event_statistics(event_id)
