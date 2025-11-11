"""Tests for Financial Aid Service"""
import pytest
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.financial_aid_service import FinancialAidService


@pytest.fixture
def financial_aid_service():
    return FinancialAidService()


@pytest.mark.asyncio
async def test_create_scholarship(db_session: AsyncSession, financial_aid_service: FinancialAidService):
    """Test creating scholarship"""
    scholarship_data = {
        "name": "Merit Scholarship",
        "amount": Decimal("50000.00"),
        "criteria": "CGPA > 9.0",
        "academic_year": "2024-25"
    }
    
    scholarship = await financial_aid_service.create_scholarship(db_session, scholarship_data)
    
    assert scholarship is not None
    assert scholarship.name == "Merit Scholarship"


@pytest.mark.asyncio
async def test_apply_for_scholarship(db_session: AsyncSession, financial_aid_service: FinancialAidService):
    """Test scholarship application"""
    application_data = {
        "student_id": uuid4(),
        "scholarship_id": uuid4(),
        "reason": "Financial need",
        "documents": ["income_certificate.pdf"]
    }
    
    application = await financial_aid_service.apply_scholarship(db_session, application_data)
    
    assert application is not None
    assert application.status == "submitted"


@pytest.mark.asyncio
async def test_approve_scholarship(db_session: AsyncSession, financial_aid_service: FinancialAidService):
    """Test approving scholarship application"""
    application_id = uuid4()
    
    approved = await financial_aid_service.approve_application(
        db_session,
        application_id=application_id,
        approved_by=uuid4(),
        approved_amount=Decimal("50000.00")
    )
    
    assert approved is not None or isinstance(approved, bool)


@pytest.mark.asyncio
async def test_check_eligibility(financial_aid_service: FinancialAidService):
    """Test scholarship eligibility check"""
    student_data = {
        "cgpa": Decimal("9.2"),
        "family_income": Decimal("300000.00"),
        "attendance_percentage": Decimal("90.0")
    }
    
    eligible = financial_aid_service.check_eligibility(
        student_data,
        min_cgpa=Decimal("9.0"),
        max_income=Decimal("500000.00")
    )
    
    assert eligible is True


@pytest.mark.asyncio
async def test_disburse_scholarship(db_session: AsyncSession, financial_aid_service: FinancialAidService):
    """Test scholarship disbursement"""
    disbursement = await financial_aid_service.disburse_scholarship(
        db_session,
        application_id=uuid4(),
        amount=Decimal("50000.00")
    )
    
    assert disbursement is not None or isinstance(disbursement, bool)


@pytest.mark.asyncio
async def test_get_student_scholarships(db_session: AsyncSession, financial_aid_service: FinancialAidService):
    """Test getting student scholarships"""
    scholarships = await financial_aid_service.get_student_scholarships(
        db_session,
        student_id=uuid4()
    )
    
    assert isinstance(scholarships, list)


@pytest.mark.asyncio
async def test_create_loan_program(db_session: AsyncSession, financial_aid_service: FinancialAidService):
    """Test creating education loan program"""
    loan_data = {
        "program_name": "Student Loan",
        "max_amount": Decimal("500000.00"),
        "interest_rate": Decimal("8.5")
    }
    
    loan = await financial_aid_service.create_loan_program(db_session, loan_data)
    
    assert loan is not None


@pytest.mark.asyncio
async def test_calculate_aid_amount(financial_aid_service: FinancialAidService):
    """Test calculating financial aid amount"""
    total_fees = Decimal("100000.00")
    family_income = Decimal("200000.00")
    
    aid_amount = financial_aid_service.calculate_aid_amount(
        total_fees,
        family_income
    )
    
    assert aid_amount >= Decimal("0.00")
