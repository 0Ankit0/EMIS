"""Hostel Service for EMIS"""
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, or_

from src.models.hostel import (
    Hostel, Room, RoomAllocation, MessMenu, HostelVisitor, HostelComplaint,
    RoomType, RoomStatus
)
from src.lib.logging import get_logger

logger = get_logger(__name__)


class HostelService:
    """Service for managing hostel operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # T139: Core hostel service
    async def create_hostel(
        self,
        hostel_name: str,
        hostel_code: str,
        gender: str,
        total_capacity: int,
        monthly_fee: float,
        warden_id: Optional[int] = None,
        **kwargs
    ) -> Hostel:
        """Create new hostel"""
        
        hostel = Hostel(
            hostel_name=hostel_name,
            hostel_code=hostel_code,
            gender=gender,
            total_capacity=total_capacity,
            monthly_fee=monthly_fee,
            warden_id=warden_id,
            **kwargs
        )
        
        self.db.add(hostel)
        await self.db.commit()
        await self.db.refresh(hostel)
        
        logger.info(f"Created hostel: {hostel_name} ({hostel_code})")
        
        return hostel
    
    async def create_room(
        self,
        hostel_id: int,
        room_number: str,
        floor: int,
        room_type: RoomType,
        bed_capacity: int,
        monthly_rent: float,
        **kwargs
    ) -> Room:
        """Create new room"""
        
        room = Room(
            hostel_id=hostel_id,
            room_number=room_number,
            floor=floor,
            room_type=room_type,
            bed_capacity=bed_capacity,
            monthly_rent=monthly_rent,
            **kwargs
        )
        
        self.db.add(room)
        await self.db.commit()
        await self.db.refresh(room)
        
        logger.info(f"Created room {room_number} in hostel {hostel_id}")
        
        return room
    
    async def get_available_rooms(
        self,
        hostel_id: Optional[int] = None,
        room_type: Optional[RoomType] = None
    ) -> List[Room]:
        """Get available rooms"""
        query = select(Room).where(Room.status == RoomStatus.AVAILABLE)
        
        if hostel_id:
            query = query.where(Room.hostel_id == hostel_id)
        
        if room_type:
            query = query.where(Room.room_type == room_type)
        
        # Also check if room has free beds
        query = query.where(Room.current_occupancy < Room.bed_capacity)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    # T140: Room allocation logic
    async def allocate_room(
        self,
        student_id: int,
        room_id: int,
        start_date: date,
        academic_year: str,
        allocated_by: Optional[int] = None,
        end_date: Optional[date] = None,
        semester: Optional[int] = None
    ) -> RoomAllocation:
        """Allocate room to student"""
        
        # Get room details
        result = await self.db.execute(
            select(Room).where(Room.id == room_id)
        )
        room = result.scalar_one_or_none()
        
        if not room:
            raise ValueError(f"Room {room_id} not found")
        
        if room.current_occupancy >= room.bed_capacity:
            raise ValueError(f"Room {room_id} is full")
        
        # Check if student already has allocation
        existing = await self.get_student_active_allocation(student_id)
        if existing:
            raise ValueError(f"Student {student_id} already has an active allocation")
        
        # Determine bed number
        bed_number = room.current_occupancy + 1
        
        # Create allocation
        allocation = RoomAllocation(
            hostel_id=room.hostel_id,
            room_id=room_id,
            student_id=student_id,
            bed_number=bed_number,
            start_date=start_date,
            end_date=end_date,
            monthly_fee=room.monthly_rent,
            academic_year=academic_year,
            semester=semester,
            allocated_by=allocated_by
        )
        
        self.db.add(allocation)
        
        # Update room occupancy
        room.current_occupancy += 1
        if room.current_occupancy >= room.bed_capacity:
            room.status = RoomStatus.OCCUPIED
        
        # Update hostel occupancy
        result = await self.db.execute(
            select(Hostel).where(Hostel.id == room.hostel_id)
        )
        hostel = result.scalar_one_or_none()
        if hostel:
            hostel.current_occupancy += 1
        
        await self.db.commit()
        await self.db.refresh(allocation)
        
        logger.info(f"Allocated room {room_id} to student {student_id}")
        
        return allocation
    
    async def deallocate_room(
        self,
        allocation_id: int,
        check_out_date: Optional[datetime] = None
    ) -> RoomAllocation:
        """Deallocate room from student"""
        
        result = await self.db.execute(
            select(RoomAllocation).where(RoomAllocation.id == allocation_id)
        )
        allocation = result.scalar_one_or_none()
        
        if not allocation:
            raise ValueError(f"Allocation {allocation_id} not found")
        
        # Mark as inactive
        allocation.is_active = False
        allocation.check_out_date = check_out_date or datetime.utcnow()
        allocation.end_date = date.today()
        
        # Update room occupancy
        result = await self.db.execute(
            select(Room).where(Room.id == allocation.room_id)
        )
        room = result.scalar_one_or_none()
        
        if room and room.current_occupancy > 0:
            room.current_occupancy -= 1
            if room.status == RoomStatus.OCCUPIED and room.current_occupancy < room.bed_capacity:
                room.status = RoomStatus.AVAILABLE
        
        # Update hostel occupancy
        result = await self.db.execute(
            select(Hostel).where(Hostel.id == allocation.hostel_id)
        )
        hostel = result.scalar_one_or_none()
        if hostel and hostel.current_occupancy > 0:
            hostel.current_occupancy -= 1
        
        await self.db.commit()
        await self.db.refresh(allocation)
        
        logger.info(f"Deallocated room for student {allocation.student_id}")
        
        return allocation
    
    async def get_student_active_allocation(
        self,
        student_id: int
    ) -> Optional[RoomAllocation]:
        """Get student's current active allocation"""
        result = await self.db.execute(
            select(RoomAllocation).where(
                and_(
                    RoomAllocation.student_id == student_id,
                    RoomAllocation.is_active == True
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def transfer_room(
        self,
        student_id: int,
        new_room_id: int,
        reason: str,
        transfer_by: Optional[int] = None
    ) -> RoomAllocation:
        """Transfer student to different room"""
        
        # Deallocate current room
        current_allocation = await self.get_student_active_allocation(student_id)
        if not current_allocation:
            raise ValueError(f"No active allocation found for student {student_id}")
        
        await self.deallocate_room(current_allocation.id)
        
        # Allocate new room
        new_allocation = await self.allocate_room(
            student_id=student_id,
            room_id=new_room_id,
            start_date=date.today(),
            academic_year=current_allocation.academic_year,
            semester=current_allocation.semester,
            allocated_by=transfer_by
        )
        
        new_allocation.notes = f"Transferred from room {current_allocation.room_id}. Reason: {reason}"
        await self.db.commit()
        
        logger.info(f"Transferred student {student_id} from room {current_allocation.room_id} to {new_room_id}")
        
        return new_allocation
    
    # T141: Mess menu management
    async def create_mess_menu(
        self,
        hostel_id: int,
        day_of_week: str,
        meal_type: str,
        menu_items: str,
        effective_from: date,
        **kwargs
    ) -> MessMenu:
        """Create mess menu"""
        
        menu = MessMenu(
            hostel_id=hostel_id,
            day_of_week=day_of_week,
            meal_type=meal_type,
            menu_items=menu_items,
            effective_from=effective_from,
            **kwargs
        )
        
        self.db.add(menu)
        await self.db.commit()
        await self.db.refresh(menu)
        
        logger.info(f"Created mess menu for {day_of_week} {meal_type} in hostel {hostel_id}")
        
        return menu
    
    async def get_weekly_mess_menu(
        self,
        hostel_id: int,
        effective_date: Optional[date] = None
    ) -> List[MessMenu]:
        """Get weekly mess menu"""
        if not effective_date:
            effective_date = date.today()
        
        result = await self.db.execute(
            select(MessMenu).where(
                and_(
                    MessMenu.hostel_id == hostel_id,
                    MessMenu.is_active == True,
                    MessMenu.effective_from <= effective_date,
                    or_(
                        MessMenu.effective_to == None,
                        MessMenu.effective_to >= effective_date
                    )
                )
            ).order_by(MessMenu.day_of_week, MessMenu.meal_type)
        )
        return result.scalars().all()
    
    async def update_mess_menu(
        self,
        menu_id: int,
        menu_items: str,
        description: Optional[str] = None
    ) -> MessMenu:
        """Update mess menu"""
        result = await self.db.execute(
            select(MessMenu).where(MessMenu.id == menu_id)
        )
        menu = result.scalar_one_or_none()
        
        if not menu:
            raise ValueError(f"Mess menu {menu_id} not found")
        
        menu.menu_items = menu_items
        if description:
            menu.description = description
        
        await self.db.commit()
        await self.db.refresh(menu)
        
        return menu
    
    # Additional hostel operations
    async def register_visitor(
        self,
        hostel_id: int,
        student_id: int,
        visitor_name: str,
        visitor_phone: Optional[str] = None,
        relationship: Optional[str] = None,
        approved_by: Optional[int] = None
    ) -> HostelVisitor:
        """Register hostel visitor"""
        
        visitor = HostelVisitor(
            hostel_id=hostel_id,
            student_id=student_id,
            visitor_name=visitor_name,
            visitor_phone=visitor_phone,
            relationship=relationship,
            check_in_time=datetime.utcnow(),
            approved_by=approved_by
        )
        
        self.db.add(visitor)
        await self.db.commit()
        await self.db.refresh(visitor)
        
        logger.info(f"Registered visitor {visitor_name} for student {student_id}")
        
        return visitor
    
    async def checkout_visitor(
        self,
        visitor_id: int
    ) -> HostelVisitor:
        """Checkout visitor"""
        result = await self.db.execute(
            select(HostelVisitor).where(HostelVisitor.id == visitor_id)
        )
        visitor = result.scalar_one_or_none()
        
        if not visitor:
            raise ValueError(f"Visitor {visitor_id} not found")
        
        visitor.check_out_time = datetime.utcnow()
        visitor.is_checked_out = True
        
        await self.db.commit()
        await self.db.refresh(visitor)
        
        return visitor
    
    async def create_complaint(
        self,
        hostel_id: int,
        student_id: int,
        category: str,
        title: str,
        description: str,
        room_id: Optional[int] = None,
        priority: str = "medium"
    ) -> HostelComplaint:
        """Create hostel complaint"""
        
        # Generate complaint number
        complaint_number = await self.generate_complaint_number(hostel_id)
        
        complaint = HostelComplaint(
            complaint_number=complaint_number,
            hostel_id=hostel_id,
            room_id=room_id,
            student_id=student_id,
            category=category,
            title=title,
            description=description,
            priority=priority
        )
        
        self.db.add(complaint)
        await self.db.commit()
        await self.db.refresh(complaint)
        
        logger.info(f"Created complaint {complaint_number}")
        
        return complaint
    
    async def generate_complaint_number(self, hostel_id: int) -> str:
        """Generate unique complaint number"""
        today = date.today()
        year_month = today.strftime("%Y%m")
        
        result = await self.db.execute(
            select(func.count(HostelComplaint.id)).where(
                HostelComplaint.complaint_number.like(f"HC{hostel_id}{year_month}%")
            )
        )
        count = result.scalar() or 0
        sequence = str(count + 1).zfill(4)
        
        return f"HC{hostel_id}{year_month}{sequence}"
    
    async def resolve_complaint(
        self,
        complaint_id: int,
        resolved_by: int,
        resolution_notes: str
    ) -> HostelComplaint:
        """Resolve hostel complaint"""
        result = await self.db.execute(
            select(HostelComplaint).where(HostelComplaint.id == complaint_id)
        )
        complaint = result.scalar_one_or_none()
        
        if not complaint:
            raise ValueError(f"Complaint {complaint_id} not found")
        
        complaint.status = "resolved"
        complaint.resolved_by = resolved_by
        complaint.resolution_notes = resolution_notes
        complaint.resolved_date = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(complaint)
        
        logger.info(f"Resolved complaint {complaint.complaint_number}")
        
        return complaint
    
    async def get_hostel_occupancy_report(
        self,
        hostel_id: Optional[int] = None
    ) -> dict:
        """Get hostel occupancy statistics"""
        query = select(Hostel)
        
        if hostel_id:
            query = query.where(Hostel.id == hostel_id)
        
        result = await self.db.execute(query)
        hostels = result.scalars().all()
        
        report = []
        total_capacity = 0
        total_occupancy = 0
        
        for hostel in hostels:
            occupancy_rate = (hostel.current_occupancy / hostel.total_capacity * 100) if hostel.total_capacity > 0 else 0
            
            report.append({
                'hostel_id': hostel.id,
                'hostel_name': hostel.hostel_name,
                'total_capacity': hostel.total_capacity,
                'current_occupancy': hostel.current_occupancy,
                'available_beds': hostel.total_capacity - hostel.current_occupancy,
                'occupancy_rate': round(occupancy_rate, 2)
            })
            
            total_capacity += hostel.total_capacity
            total_occupancy += hostel.current_occupancy
        
        overall_rate = (total_occupancy / total_capacity * 100) if total_capacity > 0 else 0
        
        return {
            'hostels': report,
            'total_capacity': total_capacity,
            'total_occupancy': total_occupancy,
            'overall_occupancy_rate': round(overall_rate, 2)
        }
