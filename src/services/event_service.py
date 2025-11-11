"""
Event Service for EMIS
Handles event management, registrations, budgets, and attendance
"""
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from src.models.event import Event, EventRegistration, EventBudget, EventAttendance, EventType, EventStatus, RegistrationStatus
from src.models.billing import Bill, BillItem, BillType
from src.lib.logging import get_logger

logger = get_logger(__name__)


class EventService:
    """Service for event management"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Event CRUD
    def create_event(self, event_data: dict, organizer_id: int) -> Event:
        """Create a new event"""
        try:
            event = Event(
                **event_data,
                organizer_id=organizer_id,
                current_participants=0
            )
            self.db.add(event)
            self.db.commit()
            self.db.refresh(event)
            logger.info(f"Event created: {event.id} - {event.title}")
            return event
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating event: {str(e)}")
            raise
    
    def get_event(self, event_id: int) -> Optional[Event]:
        """Get event by ID"""
        return self.db.query(Event).filter(Event.id == event_id).first()
    
    def get_events(
        self,
        event_type: Optional[EventType] = None,
        status: Optional[EventStatus] = None,
        department_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        is_published: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Event]:
        """Get events with filters"""
        query = self.db.query(Event)
        
        if event_type:
            query = query.filter(Event.event_type == event_type)
        if status:
            query = query.filter(Event.status == status)
        if department_id:
            query = query.filter(Event.department_id == department_id)
        if is_published is not None:
            query = query.filter(Event.is_published == is_published)
        if start_date:
            query = query.filter(Event.start_date >= start_date)
        if end_date:
            query = query.filter(Event.end_date <= end_date)
        
        return query.order_by(Event.start_date.desc()).offset(skip).limit(limit).all()
    
    def update_event(self, event_id: int, event_data: dict) -> Optional[Event]:
        """Update event"""
        try:
            event = self.get_event(event_id)
            if not event:
                return None
            
            for key, value in event_data.items():
                setattr(event, key, value)
            
            self.db.commit()
            self.db.refresh(event)
            logger.info(f"Event updated: {event_id}")
            return event
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating event: {str(e)}")
            raise
    
    def delete_event(self, event_id: int) -> bool:
        """Delete event"""
        try:
            event = self.get_event(event_id)
            if not event:
                return False
            
            self.db.delete(event)
            self.db.commit()
            logger.info(f"Event deleted: {event_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting event: {str(e)}")
            raise
    
    # Registration Management
    def register_for_event(
        self,
        event_id: int,
        participant_data: dict,
        student_id: Optional[int] = None,
        user_id: Optional[int] = None
    ) -> EventRegistration:
        """Register for an event"""
        try:
            event = self.get_event(event_id)
            if not event:
                raise ValueError("Event not found")
            
            # Check capacity
            if event.max_participants and event.current_participants >= event.max_participants:
                participant_data['status'] = RegistrationStatus.WAITLISTED
            
            # Check registration deadline
            if event.registration_end and datetime.utcnow() > event.registration_end:
                raise ValueError("Registration deadline has passed")
            
            registration = EventRegistration(
                event_id=event_id,
                student_id=student_id,
                user_id=user_id,
                **participant_data
            )
            
            self.db.add(registration)
            
            # Update participant count if approved automatically
            if not event.requires_approval:
                registration.status = RegistrationStatus.APPROVED
                event.current_participants += 1
            
            # Create bill if paid event
            if event.is_paid_event and event.registration_fee > 0 and student_id:
                self._create_event_bill(event, student_id, registration.id)
            
            self.db.commit()
            self.db.refresh(registration)
            logger.info(f"Event registration created: {registration.id} for event {event_id}")
            return registration
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error registering for event: {str(e)}")
            raise
    
    def _create_event_bill(self, event: Event, student_id: int, registration_id: int):
        """Create bill for event registration"""
        bill = Bill(
            student_id=student_id,
            bill_type=BillType.EVENT_FEE,
            due_date=event.start_date.date() if event.start_date else None,
            total_amount=event.registration_fee,
            reference_id=str(registration_id),
            description=f"Registration fee for {event.title}"
        )
        self.db.add(bill)
        
        bill_item = BillItem(
            bill=bill,
            description=f"Event: {event.title}",
            amount=event.registration_fee,
            quantity=1
        )
        self.db.add(bill_item)
    
    def approve_registration(self, registration_id: int, approved_by_id: int) -> EventRegistration:
        """Approve event registration"""
        try:
            registration = self.db.query(EventRegistration).filter(
                EventRegistration.id == registration_id
            ).first()
            
            if not registration:
                raise ValueError("Registration not found")
            
            registration.status = RegistrationStatus.APPROVED
            registration.approved_by_id = approved_by_id
            registration.approved_date = datetime.utcnow()
            
            # Update participant count
            event = registration.event
            if event.current_participants < event.max_participants:
                event.current_participants += 1
            
            self.db.commit()
            self.db.refresh(registration)
            logger.info(f"Registration approved: {registration_id}")
            return registration
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error approving registration: {str(e)}")
            raise
    
    def reject_registration(self, registration_id: int, reason: str) -> EventRegistration:
        """Reject event registration"""
        try:
            registration = self.db.query(EventRegistration).filter(
                EventRegistration.id == registration_id
            ).first()
            
            if not registration:
                raise ValueError("Registration not found")
            
            registration.status = RegistrationStatus.REJECTED
            registration.rejection_reason = reason
            
            self.db.commit()
            self.db.refresh(registration)
            logger.info(f"Registration rejected: {registration_id}")
            return registration
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error rejecting registration: {str(e)}")
            raise
    
    def get_event_registrations(
        self,
        event_id: int,
        status: Optional[RegistrationStatus] = None
    ) -> List[EventRegistration]:
        """Get registrations for an event"""
        query = self.db.query(EventRegistration).filter(EventRegistration.event_id == event_id)
        
        if status:
            query = query.filter(EventRegistration.status == status)
        
        return query.all()
    
    # Budget Management
    def add_budget_item(self, event_id: int, budget_data: dict) -> EventBudget:
        """Add budget item to event"""
        try:
            budget = EventBudget(event_id=event_id, **budget_data)
            self.db.add(budget)
            self.db.commit()
            self.db.refresh(budget)
            logger.info(f"Budget item added: {budget.id} for event {event_id}")
            return budget
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error adding budget item: {str(e)}")
            raise
    
    def approve_budget(self, budget_id: int, approved_by_id: int, approved_amount: float) -> EventBudget:
        """Approve budget item"""
        try:
            budget = self.db.query(EventBudget).filter(EventBudget.id == budget_id).first()
            if not budget:
                raise ValueError("Budget item not found")
            
            budget.is_approved = True
            budget.approved_by_id = approved_by_id
            budget.approved_date = datetime.utcnow()
            budget.approved_amount = approved_amount
            
            self.db.commit()
            self.db.refresh(budget)
            logger.info(f"Budget approved: {budget_id}")
            return budget
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error approving budget: {str(e)}")
            raise
    
    def get_event_budget_summary(self, event_id: int) -> Dict:
        """Get budget summary for event"""
        budgets = self.db.query(EventBudget).filter(EventBudget.event_id == event_id).all()
        
        total_estimated = sum(b.estimated_amount or 0 for b in budgets)
        total_approved = sum(b.approved_amount or 0 for b in budgets if b.is_approved)
        total_actual = sum(b.actual_amount or 0 for b in budgets if b.actual_amount)
        
        return {
            "total_estimated": float(total_estimated),
            "total_approved": float(total_approved),
            "total_actual": float(total_actual),
            "variance": float(total_approved - total_actual) if total_approved and total_actual else 0,
            "items": budgets
        }
    
    # Attendance Management
    def mark_attendance(
        self,
        event_id: int,
        registration_id: int,
        attendance_data: dict
    ) -> EventAttendance:
        """Mark attendance for event"""
        try:
            attendance = EventAttendance(
                event_id=event_id,
                registration_id=registration_id,
                **attendance_data,
                is_present=True
            )
            self.db.add(attendance)
            self.db.commit()
            self.db.refresh(attendance)
            logger.info(f"Attendance marked: {attendance.id} for event {event_id}")
            return attendance
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error marking attendance: {str(e)}")
            raise
    
    def get_attendance_report(self, event_id: int) -> Dict:
        """Get attendance report for event"""
        total_registered = self.db.query(func.count(EventRegistration.id)).filter(
            EventRegistration.event_id == event_id,
            EventRegistration.status == RegistrationStatus.APPROVED
        ).scalar()
        
        total_present = self.db.query(func.count(EventAttendance.id)).filter(
            EventAttendance.event_id == event_id,
            EventAttendance.is_present == True
        ).scalar()
        
        attendance_percentage = (total_present / total_registered * 100) if total_registered > 0 else 0
        
        return {
            "total_registered": total_registered,
            "total_present": total_present,
            "total_absent": total_registered - total_present,
            "attendance_percentage": round(attendance_percentage, 2)
        }
    
    # Statistics
    def get_event_statistics(self, event_id: int) -> Dict:
        """Get comprehensive statistics for event"""
        event = self.get_event(event_id)
        if not event:
            return {}
        
        registrations = self.get_event_registrations(event_id)
        budget_summary = self.get_event_budget_summary(event_id)
        attendance_report = self.get_attendance_report(event_id)
        
        return {
            "event": {
                "id": event.id,
                "title": event.title,
                "status": event.status,
                "start_date": event.start_date,
                "end_date": event.end_date
            },
            "registrations": {
                "total": len(registrations),
                "approved": len([r for r in registrations if r.status == RegistrationStatus.APPROVED]),
                "pending": len([r for r in registrations if r.status == RegistrationStatus.PENDING]),
                "rejected": len([r for r in registrations if r.status == RegistrationStatus.REJECTED]),
                "waitlisted": len([r for r in registrations if r.status == RegistrationStatus.WAITLISTED])
            },
            "budget": budget_summary,
            "attendance": attendance_report
        }
