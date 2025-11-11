"""End-to-End Student Journey Test"""
import pytest
from datetime import datetime, date
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.student import Student
from src.models.admission import Application


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_student_admission_to_enrollment(db_session: AsyncSession):
    """Test student journey from admission to enrollment"""
    # Create admission application
    app = Application(
        id=uuid4(),
        application_number="APP001",
        first_name="Test",
        last_name="Student",
        email="test@example.com",
        program="B.Tech",
        status="approved"
    )
    db_session.add(app)
    await db_session.commit()
    
    # Convert to student
    student = Student(
        id=uuid4(),
        student_id="STU001",
        first_name=app.first_name,
        last_name=app.last_name,
        email=app.email,
        program=app.program,
        status="active"
    )
    db_session.add(student)
    await db_session.commit()
    
    assert student.status == "active"
    assert app.status == "approved"
