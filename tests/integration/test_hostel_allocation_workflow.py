"""Integration tests for Hostel Allocation Workflow"""
import pytest
from datetime import datetime, date
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.student import Student
from src.models.hostel import Hostel, Room, RoomAllocation


@pytest.mark.asyncio
async def test_complete_hostel_allocation_workflow(db_session: AsyncSession):
    """Test complete hostel allocation from application to checkout"""
    # Step 1: Create hostel
    hostel = Hostel(
        id=uuid4(),
        hostel_name="Boys Hostel A",
        hostel_type="boys",
        total_rooms=100,
        occupied_rooms=0,
        warden_id=uuid4(),
        status="active"
    )
    db_session.add(hostel)
    await db_session.commit()
    
    # Step 2: Create rooms
    rooms = []
    for floor in range(1, 4):
        for room_num in range(1, 4):
            room = Room(
                id=uuid4(),
                hostel_id=hostel.id,
                room_number=f"{floor}0{room_num}",
                floor=floor,
                room_type="double",
                capacity=2,
                occupied=0,
                rent=Decimal("5000.00"),
                status="available"
            )
            db_session.add(room)
            rooms.append(room)
    await db_session.commit()
    
    # Step 3: Create student
    student = Student(
        id=uuid4(),
        student_id="STU001",
        first_name="Bob",
        last_name="Resident",
        email="bob@example.com",
        program="B.Tech",
        status="active"
    )
    db_session.add(student)
    await db_session.commit()
    
    # Step 4: Allocate room
    selected_room = rooms[0]
    allocation = RoomAllocation(
        id=uuid4(),
        room_id=selected_room.id,
        student_id=student.id,
        allocation_date=date.today(),
        status="allocated"
    )
    db_session.add(allocation)
    
    # Update room occupancy
    selected_room.occupied += 1
    if selected_room.occupied == selected_room.capacity:
        selected_room.status = "full"
    
    hostel.occupied_rooms += 1
    await db_session.commit()
    
    # Step 5: Check-in
    allocation.check_in_date = datetime.utcnow()
    allocation.status = "checked_in"
    await db_session.commit()
    
    # Step 6: Pay rent
    from src.models.billing import Bill
    bill = Bill(
        id=uuid4(),
        bill_number="HOSTEL001",
        student_id=student.id,
        billing_period="2024-Q1",
        total_amount=Decimal("5000.00"),
        paid_amount=Decimal("5000.00"),
        status="paid",
        issue_date=datetime.utcnow(),
        payment_date=datetime.utcnow()
    )
    db_session.add(bill)
    await db_session.commit()
    
    # Step 7: Check-out (end of semester)
    allocation.check_out_date = datetime.utcnow()
    allocation.status = "checked_out"
    
    # Release room
    selected_room.occupied -= 1
    selected_room.status = "available"
    hostel.occupied_rooms -= 1
    await db_session.commit()
    
    # Assertions
    assert allocation.status == "checked_out"
    assert selected_room.occupied == 0
    assert selected_room.status == "available"
    assert bill.status == "paid"
