"""Tests for HR Service"""
import pytest
from datetime import date
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.hr_service import HRService


@pytest.fixture
def hr_service():
    return HRService()


@pytest.mark.asyncio
async def test_create_employee(db_session: AsyncSession, hr_service: HRService):
    """Test creating employee"""
    employee_data = {
        "employee_id": "EMP001",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "department": "CS",
        "designation": "Professor",
        "salary": Decimal("100000.00"),
        "joining_date": date.today()
    }
    
    employee = await hr_service.create_employee(db_session, employee_data)
    
    assert employee is not None
    assert employee.employee_id == "EMP001"


@pytest.mark.asyncio
async def test_calculate_salary(hr_service: HRService):
    """Test salary calculation"""
    basic = Decimal("50000.00")
    allowances = Decimal("10000.00")
    deductions = Decimal("5000.00")
    
    net_salary = hr_service.calculate_net_salary(basic, allowances, deductions)
    
    assert net_salary == Decimal("55000.00")


@pytest.mark.asyncio
async def test_process_leave_request(db_session: AsyncSession, hr_service: HRService):
    """Test processing leave request"""
    leave_data = {
        "employee_id": uuid4(),
        "leave_type": "sick",
        "start_date": date.today(),
        "end_date": date.today(),
        "reason": "Medical"
    }
    
    leave = await hr_service.create_leave_request(db_session, leave_data)
    
    assert leave is not None
    assert leave.status == "pending"


@pytest.mark.asyncio
async def test_approve_leave(db_session: AsyncSession, hr_service: HRService):
    """Test approving leave"""
    leave_data = {
        "employee_id": uuid4(),
        "leave_type": "casual",
        "start_date": date.today(),
        "end_date": date.today()
    }
    leave = await hr_service.create_leave_request(db_session, leave_data)
    
    approved = await hr_service.approve_leave(
        db_session,
        leave_id=leave.id,
        approved_by=uuid4()
    )
    
    assert approved.status == "approved"


@pytest.mark.asyncio
async def test_generate_payslip(db_session: AsyncSession, hr_service: HRService):
    """Test generating payslip"""
    employee_id = uuid4()
    
    payslip = await hr_service.generate_payslip(
        db_session,
        employee_id=employee_id,
        month="January",
        year=2024
    )
    
    assert payslip is not None


@pytest.mark.asyncio
async def test_record_attendance(db_session: AsyncSession, hr_service: HRService):
    """Test recording employee attendance"""
    attendance_data = {
        "employee_id": uuid4(),
        "date": date.today(),
        "check_in": "09:00",
        "check_out": "17:00",
        "status": "present"
    }
    
    attendance = await hr_service.record_attendance(db_session, attendance_data)
    
    assert attendance is not None
    assert attendance.status == "present"
