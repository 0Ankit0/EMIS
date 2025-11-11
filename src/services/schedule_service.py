"""Schedule Service for managing class schedules"""
from typing import List, Optional
from datetime import date, time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from src.models.class_schedule import ClassSchedule, DayOfWeek
from src.lib.audit import audit_log


class ScheduleService:
    """Service for managing class schedules"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_schedule(
        self,
        course_id: int,
        instructor_id: Optional[int],
        day_of_week: DayOfWeek,
        start_time: time,
        end_time: time,
        effective_from: date,
        room_number: Optional[str] = None,
        building: Optional[str] = None,
        effective_to: Optional[date] = None,
        notes: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> ClassSchedule:
        """Create a new class schedule"""
        schedule = ClassSchedule(
            course_id=course_id,
            instructor_id=instructor_id,
            room_number=room_number,
            building=building,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            effective_from=effective_from,
            effective_to=effective_to,
            notes=notes
        )
        
        self.db.add(schedule)
        await self.db.commit()
        await self.db.refresh(schedule)
        
        await audit_log(
            self.db,
            action="create_schedule",
            entity_type="class_schedule",
            entity_id=schedule.id,
            user_id=user_id,
            details={"course_id": course_id, "day": day_of_week.value}
        )
        
        return schedule
    
    async def get_schedule_by_id(self, schedule_id: int) -> Optional[ClassSchedule]:
        """Get a schedule by ID"""
        result = await self.db.execute(
            select(ClassSchedule).where(ClassSchedule.id == schedule_id)
        )
        return result.scalar_one_or_none()
    
    async def get_schedules_by_course(self, course_id: int, active_only: bool = True) -> List[ClassSchedule]:
        """Get all schedules for a course"""
        query = select(ClassSchedule).where(ClassSchedule.course_id == course_id)
        
        if active_only:
            query = query.where(ClassSchedule.is_active == True)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_schedules_by_instructor(self, instructor_id: int, active_only: bool = True) -> List[ClassSchedule]:
        """Get all schedules for an instructor"""
        query = select(ClassSchedule).where(ClassSchedule.instructor_id == instructor_id)
        
        if active_only:
            query = query.where(ClassSchedule.is_active == True)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_schedules_by_day(self, day: DayOfWeek, active_only: bool = True) -> List[ClassSchedule]:
        """Get all schedules for a specific day"""
        query = select(ClassSchedule).where(ClassSchedule.day_of_week == day)
        
        if active_only:
            query = query.where(ClassSchedule.is_active == True)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def check_schedule_conflict(
        self,
        instructor_id: Optional[int],
        room_number: Optional[str],
        day_of_week: DayOfWeek,
        start_time: time,
        end_time: time,
        exclude_schedule_id: Optional[int] = None
    ) -> bool:
        """Check if there's a scheduling conflict"""
        query = select(ClassSchedule).where(
            and_(
                ClassSchedule.day_of_week == day_of_week,
                ClassSchedule.is_active == True,
                or_(
                    and_(
                        ClassSchedule.start_time <= start_time,
                        ClassSchedule.end_time > start_time
                    ),
                    and_(
                        ClassSchedule.start_time < end_time,
                        ClassSchedule.end_time >= end_time
                    ),
                    and_(
                        ClassSchedule.start_time >= start_time,
                        ClassSchedule.end_time <= end_time
                    )
                )
            )
        )
        
        if instructor_id:
            query = query.where(ClassSchedule.instructor_id == instructor_id)
        elif room_number:
            query = query.where(ClassSchedule.room_number == room_number)
        
        if exclude_schedule_id:
            query = query.where(ClassSchedule.id != exclude_schedule_id)
        
        result = await self.db.execute(query)
        conflicts = result.scalars().all()
        
        return len(conflicts) > 0
    
    async def update_schedule(
        self,
        schedule_id: int,
        updates: dict,
        user_id: Optional[int] = None
    ) -> Optional[ClassSchedule]:
        """Update a schedule"""
        schedule = await self.get_schedule_by_id(schedule_id)
        if not schedule:
            return None
        
        for key, value in updates.items():
            if hasattr(schedule, key):
                setattr(schedule, key, value)
        
        await self.db.commit()
        await self.db.refresh(schedule)
        
        await audit_log(
            self.db,
            action="update_schedule",
            entity_type="class_schedule",
            entity_id=schedule_id,
            user_id=user_id,
            details=updates
        )
        
        return schedule
    
    async def deactivate_schedule(self, schedule_id: int, user_id: Optional[int] = None) -> bool:
        """Deactivate a schedule"""
        schedule = await self.get_schedule_by_id(schedule_id)
        if not schedule:
            return False
        
        schedule.is_active = False
        await self.db.commit()
        
        await audit_log(
            self.db,
            action="deactivate_schedule",
            entity_type="class_schedule",
            entity_id=schedule_id,
            user_id=user_id
        )
        
        return True
    
    async def delete_schedule(self, schedule_id: int, user_id: Optional[int] = None) -> bool:
        """Delete a schedule"""
        schedule = await self.get_schedule_by_id(schedule_id)
        if not schedule:
            return False
        
        await self.db.delete(schedule)
        await self.db.commit()
        
        await audit_log(
            self.db,
            action="delete_schedule",
            entity_type="class_schedule",
            entity_id=schedule_id,
            user_id=user_id
        )
        
        return True
