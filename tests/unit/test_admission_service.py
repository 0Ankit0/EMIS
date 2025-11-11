"""Comprehensive tests for Admission Service"""
import pytest
from datetime import datetime, date
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.admission import Application, AdmissionTest, MeritList
from src.services.admission_service import AdmissionService


@pytest.fixture
def admission_service():
    """Create admission service instance"""
    return AdmissionService()


@pytest.mark.asyncio
async def test_create_application(db_session: AsyncSession, admission_service: AdmissionService):
    """Test creating a new admission application"""
    application_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "date_of_birth": date(2005, 1, 1),
        "program": "B.Tech",
        "previous_marks": Decimal("85.5")
    }
    
    application = await admission_service.create_application(db_session, application_data)
    
    assert application is not None
    assert application.first_name == "John"
    assert application.email == "john.doe@example.com"
    assert application.status == "submitted"
    assert application.application_number is not None


@pytest.mark.asyncio
async def test_get_application_by_id(
    db_session: AsyncSession,
    admission_service: AdmissionService
):
    """Test retrieving application by ID"""
    # Create application
    app_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "phone": "9876543210",
        "program": "MBA",
        "previous_marks": Decimal("90.0")
    }
    created_app = await admission_service.create_application(db_session, app_data)
    
    # Retrieve it
    application = await admission_service.get_application_by_id(
        db_session,
        created_app.id
    )
    
    assert application is not None
    assert application.id == created_app.id
    assert application.email == "jane@example.com"


@pytest.mark.asyncio
async def test_update_application_status(
    db_session: AsyncSession,
    admission_service: AdmissionService
):
    """Test updating application status"""
    # Create application
    app_data = {
        "first_name": "Bob",
        "last_name": "Wilson",
        "email": "bob@example.com",
        "phone": "1111111111",
        "program": "M.Tech",
        "previous_marks": Decimal("88.0")
    }
    application = await admission_service.create_application(db_session, app_data)
    
    # Update status
    updated = await admission_service.update_status(
        db_session,
        application_id=application.id,
        new_status="under_review"
    )
    
    assert updated.status == "under_review"


@pytest.mark.asyncio
async def test_verify_documents(
    db_session: AsyncSession,
    admission_service: AdmissionService
):
    """Test document verification"""
    app_data = {
        "first_name": "Alice",
        "last_name": "Brown",
        "email": "alice@example.com",
        "phone": "2222222222",
        "program": "BBA",
        "previous_marks": Decimal("82.0")
    }
    application = await admission_service.create_application(db_session, app_data)
    
    # Verify documents
    success = await admission_service.verify_documents(
        db_session,
        application_id=application.id,
        verified_by=uuid4(),
        documents_valid=True
    )
    
    assert success is True
    
    # Check status updated
    updated_app = await admission_service.get_application_by_id(
        db_session,
        application.id
    )
    assert updated_app.documents_verified is True


@pytest.mark.asyncio
async def test_schedule_admission_test(
    db_session: AsyncSession,
    admission_service: AdmissionService
):
    """Test scheduling admission test"""
    app_data = {
        "first_name": "Charlie",
        "last_name": "Davis",
        "email": "charlie@example.com",
        "phone": "3333333333",
        "program": "M.Sc",
        "previous_marks": Decimal("87.0")
    }
    application = await admission_service.create_application(db_session, app_data)
    
    test_data = {
        "test_date": datetime(2024, 6, 15, 10, 0),
        "venue": "Main Campus Hall A",
        "duration_minutes": 120
    }
    
    test = await admission_service.schedule_test(
        db_session,
        application_id=application.id,
        **test_data
    )
    
    assert test is not None
    assert test.application_id == application.id
    assert test.venue == "Main Campus Hall A"


@pytest.mark.asyncio
async def test_submit_test_score(
    db_session: AsyncSession,
    admission_service: AdmissionService
):
    """Test submitting admission test score"""
    # Create application and schedule test
    app_data = {
        "first_name": "David",
        "last_name": "Miller",
        "email": "david@example.com",
        "phone": "4444444444",
        "program": "MCA",
        "previous_marks": Decimal("85.0")
    }
    application = await admission_service.create_application(db_session, app_data)
    
    test = await admission_service.schedule_test(
        db_session,
        application_id=application.id,
        test_date=datetime(2024, 6, 15, 10, 0),
        venue="Hall B",
        duration_minutes=90
    )
    
    # Submit score
    updated_test = await admission_service.submit_test_score(
        db_session,
        test_id=test.id,
        score=Decimal("78.5"),
        max_score=Decimal("100.0")
    )
    
    assert updated_test.score == Decimal("78.5")
    assert updated_test.max_score == Decimal("100.0")


@pytest.mark.asyncio
async def test_calculate_merit_score(
    db_session: AsyncSession,
    admission_service: AdmissionService
):
    """Test merit score calculation"""
    previous_marks = Decimal("85.0")
    test_score = Decimal("78.0")
    
    merit_score = admission_service.calculate_merit_score(
        previous_marks=previous_marks,
        test_score=test_score,
        previous_weight=0.6,
        test_weight=0.4
    )
    
    # (85 * 0.6) + (78 * 0.4) = 51 + 31.2 = 82.2
    assert merit_score == Decimal("82.2")


@pytest.mark.asyncio
async def test_generate_merit_list(
    db_session: AsyncSession,
    admission_service: AdmissionService
):
    """Test generating merit list"""
    # Create multiple applications
    for i in range(5):
        app_data = {
            "first_name": f"Student{i}",
            "last_name": "Test",
            "email": f"student{i}@example.com",
            "phone": f"555000000{i}",
            "program": "B.Tech",
            "previous_marks": Decimal(f"{80 + i}.0")
        }
        await admission_service.create_application(db_session, app_data)
    
    # Generate merit list
    merit_list = await admission_service.generate_merit_list(
        db_session,
        program="B.Tech",
        academic_year="2024-25",
        seats_available=3
    )
    
    assert merit_list is not None
    assert len(merit_list.entries) <= 3  # Only top 3


@pytest.mark.asyncio
async def test_approve_application(
    db_session: AsyncSession,
    admission_service: AdmissionService
):
    """Test approving an application"""
    app_data = {
        "first_name": "Emma",
        "last_name": "Wilson",
        "email": "emma@example.com",
        "phone": "6666666666",
        "program": "B.Sc",
        "previous_marks": Decimal("92.0")
    }
    application = await admission_service.create_application(db_session, app_data)
    
    # Approve
    success = await admission_service.approve_application(
        db_session,
        application_id=application.id,
        approved_by=uuid4()
    )
    
    assert success is True
    
    # Verify status
    updated_app = await admission_service.get_application_by_id(
        db_session,
        application.id
    )
    assert updated_app.status == "approved"


@pytest.mark.asyncio
async def test_reject_application(
    db_session: AsyncSession,
    admission_service: AdmissionService
):
    """Test rejecting an application"""
    app_data = {
        "first_name": "Frank",
        "last_name": "Jones",
        "email": "frank@example.com",
        "phone": "7777777777",
        "program": "MBA",
        "previous_marks": Decimal("60.0")
    }
    application = await admission_service.create_application(db_session, app_data)
    
    # Reject
    success = await admission_service.reject_application(
        db_session,
        application_id=application.id,
        rejected_by=uuid4(),
        reason="Does not meet minimum criteria"
    )
    
    assert success is True
    
    # Verify status
    updated_app = await admission_service.get_application_by_id(
        db_session,
        application.id
    )
    assert updated_app.status == "rejected"
    assert "minimum criteria" in updated_app.rejection_reason


@pytest.mark.asyncio
async def test_get_applications_by_status(
    db_session: AsyncSession,
    admission_service: AdmissionService
):
    """Test getting applications by status"""
    # Create applications with different statuses
    statuses = ["submitted", "under_review", "approved", "rejected"]
    
    for i, status in enumerate(statuses):
        app_data = {
            "first_name": f"Applicant{i}",
            "last_name": "Test",
            "email": f"applicant{i}@example.com",
            "phone": f"888000000{i}",
            "program": "B.Tech",
            "previous_marks": Decimal("80.0")
        }
        app = await admission_service.create_application(db_session, app_data)
        await admission_service.update_status(db_session, app.id, status)
    
    # Get submitted applications
    submitted_apps = await admission_service.get_applications_by_status(
        db_session,
        status="submitted"
    )
    
    assert len(submitted_apps) >= 1
    assert all(app.status == "submitted" for app in submitted_apps)


@pytest.mark.asyncio
async def test_search_applications(
    db_session: AsyncSession,
    admission_service: AdmissionService
):
    """Test searching applications"""
    app_data = {
        "first_name": "SearchTest",
        "last_name": "User",
        "email": "searchtest@example.com",
        "phone": "9999999999",
        "program": "B.Tech",
        "previous_marks": Decimal("85.0")
    }
    await admission_service.create_application(db_session, app_data)
    
    # Search by name
    results = await admission_service.search_applications(
        db_session,
        query="SearchTest"
    )
    
    assert len(results) >= 1
    assert any(app.first_name == "SearchTest" for app in results)


@pytest.mark.asyncio
async def test_generate_offer_letter(
    db_session: AsyncSession,
    admission_service: AdmissionService
):
    """Test generating offer letter"""
    app_data = {
        "first_name": "OfferTest",
        "last_name": "Student",
        "email": "offer@example.com",
        "phone": "1010101010",
        "program": "M.Tech",
        "previous_marks": Decimal("88.0")
    }
    application = await admission_service.create_application(db_session, app_data)
    await admission_service.approve_application(db_session, application.id, uuid4())
    
    # Generate offer letter
    offer_letter = await admission_service.generate_offer_letter(
        db_session,
        application_id=application.id
    )
    
    assert offer_letter is not None
    assert application.first_name in offer_letter
    assert application.program in offer_letter


@pytest.mark.asyncio
async def test_get_admission_statistics(
    db_session: AsyncSession,
    admission_service: AdmissionService
):
    """Test getting admission statistics"""
    # Create some applications
    for i in range(10):
        app_data = {
            "first_name": f"Stats{i}",
            "last_name": "Test",
            "email": f"stats{i}@example.com",
            "phone": f"111000000{i}",
            "program": "B.Tech",
            "previous_marks": Decimal("80.0")
        }
        await admission_service.create_application(db_session, app_data)
    
    # Get statistics
    stats = await admission_service.get_statistics(
        db_session,
        academic_year="2024-25"
    )
    
    assert stats is not None
    assert "total_applications" in stats
    assert stats["total_applications"] >= 10


@pytest.mark.asyncio
async def test_check_eligibility(admission_service: AdmissionService):
    """Test eligibility checking"""
    # Eligible candidate
    eligible = admission_service.check_eligibility(
        program="B.Tech",
        previous_marks=Decimal("85.0"),
        min_required=Decimal("75.0")
    )
    assert eligible is True
    
    # Not eligible
    not_eligible = admission_service.check_eligibility(
        program="B.Tech",
        previous_marks=Decimal("70.0"),
        min_required=Decimal("75.0")
    )
    assert not_eligible is False


@pytest.mark.asyncio
async def test_send_admission_confirmation(
    db_session: AsyncSession,
    admission_service: AdmissionService
):
    """Test sending admission confirmation"""
    app_data = {
        "first_name": "Confirm",
        "last_name": "Test",
        "email": "confirm@example.com",
        "phone": "1212121212",
        "program": "MBA",
        "previous_marks": Decimal("90.0")
    }
    application = await admission_service.create_application(db_session, app_data)
    await admission_service.approve_application(db_session, application.id, uuid4())
    
    # Send confirmation
    success = await admission_service.send_confirmation_email(
        db_session,
        application_id=application.id
    )
    
    assert success is True
