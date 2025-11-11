"""Schedule API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date, time
from pydantic import BaseModel

from src.database import get_db
from src.services.schedule_service import ScheduleService
from src.models.class_schedule import DayOfWeek
from src.middleware.rbac import require_permissions

router = APIRouter(prefix="/schedules", tags=["schedules"])


class ScheduleCreate(BaseModel):
    course_id: int
    instructor_id: Optional[int] = None
    day_of_week: DayOfWeek
    start_time: time
    end_time: time
    effective_from: date
    room_number: Optional[str] = None
    building: Optional[str] = None
    effective_to: Optional[date] = None
    notes: Optional[str] = None


class ScheduleUpdate(BaseModel):
    instructor_id: Optional[int] = None
    day_of_week: Optional[DayOfWeek] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    room_number: Optional[str] = None
    building: Optional[str] = None
    effective_to: Optional[date] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class ScheduleResponse(BaseModel):
    id: int
    course_id: int
    instructor_id: Optional[int]
    room_number: Optional[str]
    building: Optional[str]
    day_of_week: DayOfWeek
    start_time: time
    end_time: time
    effective_from: date
    effective_to: Optional[date]
    is_active: bool
    notes: Optional[str]

    class Config:
        from_attributes = True


@router.post("/", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule_data: ScheduleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["schedule:create"]))
):
    """Create a new class schedule"""
    service = ScheduleService(db)
    
    # Check for conflicts
    has_conflict = await service.check_schedule_conflict(
        instructor_id=schedule_data.instructor_id,
        room_number=schedule_data.room_number,
        day_of_week=schedule_data.day_of_week,
        start_time=schedule_data.start_time,
        end_time=schedule_data.end_time
    )
    
    if has_conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Schedule conflict detected for instructor or room"
        )
    
    schedule = await service.create_schedule(
        **schedule_data.dict(),
        user_id=current_user.get("id")
    )
    
    return schedule


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["schedule:read"]))
):
    """Get a schedule by ID"""
    service = ScheduleService(db)
    schedule = await service.get_schedule_by_id(schedule_id)
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    
    return schedule


@router.get("/course/{course_id}", response_model=List[ScheduleResponse])
async def get_schedules_by_course(
    course_id: int,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["schedule:read"]))
):
    """Get all schedules for a course"""
    service = ScheduleService(db)
    schedules = await service.get_schedules_by_course(course_id, active_only)
    return schedules


@router.get("/instructor/{instructor_id}", response_model=List[ScheduleResponse])
async def get_schedules_by_instructor(
    instructor_id: int,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["schedule:read"]))
):
    """Get all schedules for an instructor"""
    service = ScheduleService(db)
    schedules = await service.get_schedules_by_instructor(instructor_id, active_only)
    return schedules


@router.get("/day/{day}", response_model=List[ScheduleResponse])
async def get_schedules_by_day(
    day: DayOfWeek,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["schedule:read"]))
):
    """Get all schedules for a specific day"""
    service = ScheduleService(db)
    schedules = await service.get_schedules_by_day(day, active_only)
    return schedules


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: int,
    schedule_data: ScheduleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["schedule:update"]))
):
    """Update a schedule"""
    service = ScheduleService(db)
    
    updates = schedule_data.dict(exclude_unset=True)
    
    if any(k in updates for k in ["day_of_week", "start_time", "end_time", "instructor_id", "room_number"]):
        existing = await service.get_schedule_by_id(schedule_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Schedule not found"
            )
        
        check_instructor = updates.get("instructor_id", existing.instructor_id)
        check_room = updates.get("room_number", existing.room_number)
        check_day = updates.get("day_of_week", existing.day_of_week)
        check_start = updates.get("start_time", existing.start_time)
        check_end = updates.get("end_time", existing.end_time)
        
        has_conflict = await service.check_schedule_conflict(
            instructor_id=check_instructor,
            room_number=check_room,
            day_of_week=check_day,
            start_time=check_start,
            end_time=check_end,
            exclude_schedule_id=schedule_id
        )
        
        if has_conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Schedule conflict detected for instructor or room"
            )
    
    schedule = await service.update_schedule(
        schedule_id,
        updates,
        user_id=current_user.get("id")
    )
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    
    return schedule


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["schedule:delete"]))
):
    """Delete a schedule"""
    service = ScheduleService(db)
    success = await service.delete_schedule(schedule_id, user_id=current_user.get("id"))
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    
    return None
