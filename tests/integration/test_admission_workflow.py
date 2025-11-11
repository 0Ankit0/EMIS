"""Integration tests for Admission Workflow"""
import pytest
from datetime import datetime, date
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.admission import Application
from src.models.student import Student


@pytest.mark.asyncio
async def test_complete_admission_process(db_session: AsyncSession):
    """Test complete admission workflow from application to enrollment"""
    # Step 1: Submit application
    application = Application(
        id=uuid4(),
        application_number="APP2024001",
        first_name="John",
        last_name="Applicant",
        email="john.applicant@example.com",
        phone="1234567890",
        date_of_birth=date(2005, 1, 1),
        program="B.Tech",
        previous_marks=Decimal("85.0"),
        status="submitted"
    )
    db_session.add(application)
    await db_session.commit()
    
    # Step 2: Document verification
    application.documents_verified = True
    application.status = "verified"
    await db_session.commit()
    
    # Step 3: Admission test
    application.test_score = Decimal("78.0")
    application.status = "test_completed"
    await db_session.commit()
    
    # Step 4: Merit list inclusion
    merit_score = (application.previous_marks * Decimal("0.6")) + (application.test_score * Decimal("0.4"))
    application.merit_score = merit_score
    application.status = "selected"
    await db_session.commit()
    
    # Step 5: Approval
    application.status = "approved"
    application.approved_at = datetime.utcnow()
    await db_session.commit()
    
    # Step 6: Convert to student
    student = Student(
        id=uuid4(),
        student_id="STU2024001",
        first_name=application.first_name,
        last_name=application.last_name,
        email=application.email,
        phone=application.phone,
        date_of_birth=application.date_of_birth,
        program=application.program,
        admission_date=datetime.utcnow(),
        status="active"
    )
    db_session.add(student)
    
    application.status = "enrolled"
    application.student_id = student.id
    await db_session.commit()
    await db_session.refresh(student)
    
    # Assertions
    assert application.status == "enrolled"
    assert student.student_id == "STU2024001"
    assert student.program == "B.Tech"


@pytest.mark.asyncio
async def test_rejection_workflow(db_session: AsyncSession):
    """Test application rejection workflow"""
    application = Application(
        id=uuid4(),
        application_number="APP2024002",
        first_name="Jane",
        last_name="Rejected",
        email="jane.rejected@example.com",
        phone="9876543210",
        program="MBA",
        previous_marks=Decimal("60.0"),
        status="submitted"
    )
    db_session.add(application)
    await db_session.commit()
    
    # Reject due to low marks
    application.status = "rejected"
    application.rejection_reason = "Does not meet minimum criteria"
    application.rejected_at = datetime.utcnow()
    await db_session.commit()
    
    assert application.status == "rejected"
    assert application.rejection_reason is not None
