"""Integration tests for Transport Workflow"""
import pytest
from datetime import date, time
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.student import Student
from src.models.transport import Bus, Route, RouteStop, StudentTransport


@pytest.mark.asyncio
async def test_complete_transport_workflow(db_session: AsyncSession):
    """Test complete transport workflow from route creation to assignment"""
    # Step 1: Create bus
    bus = Bus(
        id=uuid4(),
        bus_number="TN01AB1234",
        capacity=50,
        driver_name="John Driver",
        driver_phone="9876543210",
        status="active"
    )
    db_session.add(bus)
    await db_session.commit()
    
    # Step 2: Create route
    route = Route(
        id=uuid4(),
        route_name="Route 1 - North",
        route_code="R001",
        start_point="University",
        end_point="City Center",
        distance_km=Decimal("25.0"),
        estimated_time_minutes=45,
        monthly_fee=Decimal("2000.00"),
        status="active"
    )
    db_session.add(route)
    await db_session.commit()
    
    # Step 3: Add stops to route
    stops = [
        {"name": "University Gate", "order": 1, "pickup_time": time(7, 0)},
        {"name": "Main Road Junction", "order": 2, "pickup_time": time(7, 15)},
        {"name": "Market Square", "order": 3, "pickup_time": time(7, 30)},
        {"name": "City Center", "order": 4, "pickup_time": time(7, 45)}
    ]
    
    for stop_data in stops:
        stop = RouteStop(
            id=uuid4(),
            route_id=route.id,
            stop_name=stop_data["name"],
            stop_order=stop_data["order"],
            pickup_time=stop_data["pickup_time"],
            drop_time=time(17, 30)  # Return time
        )
        db_session.add(stop)
    await db_session.commit()
    
    # Step 4: Assign bus to route
    route.bus_id = bus.id
    await db_session.commit()
    
    # Step 5: Create students
    students = []
    for i in range(10):
        student = Student(
            id=uuid4(),
            student_id=f"STU00{i+1}",
            first_name=f"Student{i+1}",
            last_name="Commuter",
            email=f"student{i+1}@example.com",
            program="B.Tech",
            status="active"
        )
        db_session.add(student)
        students.append(student)
    await db_session.commit()
    
    # Step 6: Assign students to transport
    assignments = []
    for i, student in enumerate(students):
        assignment = StudentTransport(
            id=uuid4(),
            student_id=student.id,
            route_id=route.id,
            stop_id=stops[i % len(stops)]["order"],  # Distribute across stops
            start_date=date.today(),
            monthly_fee=route.monthly_fee,
            status="active"
        )
        db_session.add(assignment)
        assignments.append(assignment)
    
    bus.current_occupancy = len(students)
    await db_session.commit()
    
    # Assertions
    assert bus.current_occupancy == 10
    assert bus.current_occupancy <= bus.capacity
    assert len(assignments) == 10
    assert all(a.status == "active" for a in assignments)
