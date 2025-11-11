"""Hostel Management API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date, time
from pydantic import BaseModel

from src.database import get_db
from src.services.hostel_service import HostelService
from src.models.hostel import RoomType, RoomStatus
from src.middleware.rbac import require_permissions

router = APIRouter(prefix="/hostel", tags=["hostel"])


# Pydantic models for requests/responses
class HostelCreate(BaseModel):
    hostel_name: str
    hostel_code: str
    gender: str
    total_capacity: int
    monthly_fee: float
    warden_id: Optional[int] = None
    has_mess: bool = False
    has_gym: bool = False
    description: Optional[str] = None


class RoomCreate(BaseModel):
    hostel_id: int
    room_number: str
    floor: int
    room_type: RoomType
    bed_capacity: int
    monthly_rent: float
    has_ac: bool = False
    has_attached_bathroom: bool = True


class RoomAllocationCreate(BaseModel):
    student_id: int
    room_id: int
    start_date: date
    academic_year: str
    end_date: Optional[date] = None
    semester: Optional[int] = None


class MessMenuCreate(BaseModel):
    hostel_id: int
    day_of_week: str
    meal_type: str
    menu_items: str
    effective_from: date
    description: Optional[str] = None
    is_vegetarian: bool = True


class VisitorRegister(BaseModel):
    hostel_id: int
    student_id: int
    visitor_name: str
    visitor_phone: Optional[str] = None
    relationship: Optional[str] = None


class ComplaintCreate(BaseModel):
    hostel_id: int
    student_id: int
    category: str
    title: str
    description: str
    room_id: Optional[int] = None
    priority: str = "medium"


# T142: Hostel management endpoints
@router.post("/hostels", status_code=status.HTTP_201_CREATED)
async def create_hostel(
    hostel_data: HostelCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hostel:admin"]))
):
    """Create new hostel"""
    service = HostelService(db)
    hostel = await service.create_hostel(**hostel_data.dict())
    return {
        "id": hostel.id,
        "hostel_name": hostel.hostel_name,
        "hostel_code": hostel.hostel_code,
        "total_capacity": hostel.total_capacity
    }


@router.post("/rooms", status_code=status.HTTP_201_CREATED)
async def create_room(
    room_data: RoomCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hostel:admin"]))
):
    """Create new room"""
    service = HostelService(db)
    room = await service.create_room(**room_data.dict())
    return {
        "id": room.id,
        "room_number": room.room_number,
        "hostel_id": room.hostel_id,
        "bed_capacity": room.bed_capacity,
        "status": room.status
    }


@router.get("/rooms/available")
async def get_available_rooms(
    hostel_id: Optional[int] = None,
    room_type: Optional[RoomType] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hostel:read"]))
):
    """Get available rooms"""
    service = HostelService(db)
    rooms = await service.get_available_rooms(hostel_id, room_type)
    return {
        "rooms": [
            {
                "id": r.id,
                "room_number": r.room_number,
                "hostel_id": r.hostel_id,
                "room_type": r.room_type,
                "bed_capacity": r.bed_capacity,
                "current_occupancy": r.current_occupancy,
                "available_beds": r.bed_capacity - r.current_occupancy,
                "monthly_rent": r.monthly_rent
            }
            for r in rooms
        ]
    }


# T143: Room allocation endpoints
@router.post("/allocations", status_code=status.HTTP_201_CREATED)
async def allocate_room(
    allocation_data: RoomAllocationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hostel:allocate"]))
):
    """Allocate room to student (T140)"""
    service = HostelService(db)
    
    try:
        allocation = await service.allocate_room(
            **allocation_data.dict(),
            allocated_by=current_user.get("id")
        )
        return {
            "id": allocation.id,
            "student_id": allocation.student_id,
            "room_id": allocation.room_id,
            "bed_number": allocation.bed_number,
            "start_date": allocation.start_date,
            "monthly_fee": allocation.monthly_fee
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/allocations/{allocation_id}/deallocate")
async def deallocate_room(
    allocation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hostel:allocate"]))
):
    """Deallocate room from student (T140)"""
    service = HostelService(db)
    
    try:
        allocation = await service.deallocate_room(allocation_id)
        return {
            "id": allocation.id,
            "student_id": allocation.student_id,
            "check_out_date": allocation.check_out_date,
            "is_active": allocation.is_active
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/allocations/transfer")
async def transfer_room(
    student_id: int,
    new_room_id: int,
    reason: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hostel:allocate"]))
):
    """Transfer student to different room (T140)"""
    service = HostelService(db)
    
    try:
        allocation = await service.transfer_room(
            student_id=student_id,
            new_room_id=new_room_id,
            reason=reason,
            transfer_by=current_user.get("id")
        )
        return {
            "id": allocation.id,
            "student_id": allocation.student_id,
            "room_id": allocation.room_id,
            "notes": allocation.notes
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/allocations/student/{student_id}")
async def get_student_allocation(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hostel:read"]))
):
    """Get student's current allocation (T140)"""
    service = HostelService(db)
    allocation = await service.get_student_active_allocation(student_id)
    
    if not allocation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No active allocation found for student {student_id}"
        )
    
    return {
        "id": allocation.id,
        "hostel_id": allocation.hostel_id,
        "room_id": allocation.room_id,
        "bed_number": allocation.bed_number,
        "start_date": allocation.start_date,
        "monthly_fee": allocation.monthly_fee,
        "is_active": allocation.is_active
    }


# Mess menu endpoints
@router.post("/mess-menu", status_code=status.HTTP_201_CREATED)
async def create_mess_menu(
    menu_data: MessMenuCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hostel:admin"]))
):
    """Create mess menu (T141)"""
    service = HostelService(db)
    menu = await service.create_mess_menu(**menu_data.dict())
    return {
        "id": menu.id,
        "day_of_week": menu.day_of_week,
        "meal_type": menu.meal_type,
        "menu_items": menu.menu_items
    }


@router.get("/mess-menu/{hostel_id}/weekly")
async def get_weekly_mess_menu(
    hostel_id: int,
    effective_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hostel:read"]))
):
    """Get weekly mess menu (T141)"""
    service = HostelService(db)
    menus = await service.get_weekly_mess_menu(hostel_id, effective_date)
    return {
        "menus": [
            {
                "id": m.id,
                "day_of_week": m.day_of_week,
                "meal_type": m.meal_type,
                "menu_items": m.menu_items,
                "description": m.description,
                "is_vegetarian": m.is_vegetarian
            }
            for m in menus
        ]
    }


# Visitor management
@router.post("/visitors", status_code=status.HTTP_201_CREATED)
async def register_visitor(
    visitor_data: VisitorRegister,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hostel:manage"]))
):
    """Register hostel visitor"""
    service = HostelService(db)
    visitor = await service.register_visitor(
        **visitor_data.dict(),
        approved_by=current_user.get("id")
    )
    return {
        "id": visitor.id,
        "visitor_name": visitor.visitor_name,
        "check_in_time": visitor.check_in_time
    }


@router.post("/visitors/{visitor_id}/checkout")
async def checkout_visitor(
    visitor_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hostel:manage"]))
):
    """Checkout visitor"""
    service = HostelService(db)
    visitor = await service.checkout_visitor(visitor_id)
    return {
        "id": visitor.id,
        "check_out_time": visitor.check_out_time,
        "is_checked_out": visitor.is_checked_out
    }


# Complaint management
@router.post("/complaints", status_code=status.HTTP_201_CREATED)
async def create_complaint(
    complaint_data: ComplaintCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hostel:complaint"]))
):
    """Create hostel complaint"""
    service = HostelService(db)
    complaint = await service.create_complaint(**complaint_data.dict())
    return {
        "id": complaint.id,
        "complaint_number": complaint.complaint_number,
        "category": complaint.category,
        "title": complaint.title,
        "priority": complaint.priority,
        "status": complaint.status
    }


@router.post("/complaints/{complaint_id}/resolve")
async def resolve_complaint(
    complaint_id: int,
    resolution_notes: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hostel:admin"]))
):
    """Resolve hostel complaint"""
    service = HostelService(db)
    
    try:
        complaint = await service.resolve_complaint(
            complaint_id=complaint_id,
            resolved_by=current_user.get("id"),
            resolution_notes=resolution_notes
        )
        return {
            "id": complaint.id,
            "complaint_number": complaint.complaint_number,
            "status": complaint.status,
            "resolved_date": complaint.resolved_date
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# Reports
@router.get("/occupancy-report")
async def get_occupancy_report(
    hostel_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["hostel:read"]))
):
    """Get hostel occupancy report"""
    service = HostelService(db)
    report = await service.get_hostel_occupancy_report(hostel_id)
    return report
