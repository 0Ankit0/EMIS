"""Integration tests for Placement Workflow"""
import pytest
from datetime import datetime, date
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.student import Student
from src.models.placement import Company, PlacementDrive, StudentRegistration, PlacementOffer


@pytest.mark.asyncio
async def test_complete_placement_workflow(db_session: AsyncSession):
    """Test complete placement workflow from drive to offer"""
    # Step 1: Register company
    company = Company(
        id=uuid4(),
        company_name="TechCorp Inc",
        industry="IT",
        contact_email="hr@techcorp.com",
        contact_phone="1234567890",
        website="www.techcorp.com",
        status="active"
    )
    db_session.add(company)
    await db_session.commit()
    
    # Step 2: Schedule placement drive
    drive = PlacementDrive(
        id=uuid4(),
        company_id=company.id,
        drive_date=date(2024, 9, 15),
        job_role="Software Engineer",
        ctc=Decimal("1200000.00"),
        eligibility_criteria="CGPA >= 7.0",
        max_registrations=100,
        status="scheduled"
    )
    db_session.add(drive)
    await db_session.commit()
    
    # Step 3: Create eligible students
    students = []
    for i in range(5):
        student = Student(
            id=uuid4(),
            student_id=f"STU00{i+1}",
            first_name=f"Student{i+1}",
            last_name="Candidate",
            email=f"student{i+1}@example.com",
            program="B.Tech",
            cgpa=Decimal("8.5"),
            status="active"
        )
        db_session.add(student)
        students.append(student)
    await db_session.commit()
    
    # Step 4: Students register for drive
    registrations = []
    for student in students:
        registration = StudentRegistration(
            id=uuid4(),
            drive_id=drive.id,
            student_id=student.id,
            registration_date=datetime.utcnow(),
            status="registered"
        )
        db_session.add(registration)
        registrations.append(registration)
    
    drive.registered_count = len(students)
    await db_session.commit()
    
    # Step 5: Conduct tests/interviews
    for registration in registrations[:3]:  # First 3 clear
        registration.test_score = Decimal("85.0")
        registration.status = "shortlisted"
    
    for registration in registrations[3:]:  # Last 2 don't clear
        registration.test_score = Decimal("55.0")
        registration.status = "rejected"
    
    await db_session.commit()
    
    # Step 6: Make offers
    offers = []
    for registration in registrations[:2]:  # First 2 get offers
        offer = PlacementOffer(
            id=uuid4(),
            registration_id=registration.id,
            student_id=registration.student_id,
            company_id=company.id,
            job_role=drive.job_role,
            ctc=drive.ctc,
            offer_date=datetime.utcnow(),
            status="offered"
        )
        db_session.add(offer)
        offers.append(offer)
        registration.status = "offered"
    
    await db_session.commit()
    
    # Step 7: Students accept offers
    for offer in offers:
        offer.status = "accepted"
        offer.acceptance_date = datetime.utcnow()
        
        # Update student placement status
        student = next(s for s in students if s.id == offer.student_id)
        student.placement_status = "placed"
        student.placement_company = company.company_name
        student.placement_ctc = offer.ctc
    
    await db_session.commit()
    
    # Assertions
    assert drive.registered_count == 5
    assert len(offers) == 2
    assert all(o.status == "accepted" for o in offers)
    assert sum(1 for s in students if s.placement_status == "placed") == 2
