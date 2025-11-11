"""Payroll API routes for EMIS."""
from datetime import date
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.middleware.rbac import require_permissions
from src.models.auth import User
from src.models.payroll import Payroll, PayrollStatus


router = APIRouter(prefix="/api/v1/hr/payroll", tags=["Payroll"])


class PayrollCreate(BaseModel):
    employee_id: UUID
    month: str
    year: int
    pay_period_start: date
    pay_period_end: date
    basic_salary: float
    hra: Optional[float] = 0
    transport_allowance: Optional[float] = 0
    medical_allowance: Optional[float] = 0
    special_allowance: Optional[float] = 0
    provident_fund: Optional[float] = 0
    professional_tax: Optional[float] = 0
    income_tax: Optional[float] = 0


class PayrollResponse(BaseModel):
    id: UUID
    employee_id: UUID
    month: str
    year: int
    basic_salary: float
    gross_salary: float
    total_deductions: float
    net_salary: float
    status: str
    payment_date: Optional[date]

    class Config:
        from_attributes = True


@router.post("/", response_model=PayrollResponse, status_code=status.HTTP_201_CREATED)
async def create_payroll(
    payroll_data: PayrollCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("payroll:create")),
):
    """Create a payroll record."""
    payroll = Payroll(**payroll_data.dict())
    
    # Calculate totals
    payroll.gross_salary = payroll.calculate_gross_salary()
    payroll.total_deductions = payroll.calculate_total_deductions()
    payroll.net_salary = payroll.calculate_net_salary()

    db.add(payroll)
    await db.commit()
    await db.refresh(payroll)

    return payroll


@router.get("/{payroll_id}", response_model=PayrollResponse)
async def get_payroll(
    payroll_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("payroll:read")),
):
    """Get payroll by ID."""
    payroll = await db.get(Payroll, payroll_id)

    if not payroll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payroll not found"
        )

    return payroll


@router.post("/{payroll_id}/process")
async def process_payroll(
    payroll_id: UUID,
    payment_date: date,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("payroll:process")),
):
    """Process payroll payment."""
    payroll = await db.get(Payroll, payroll_id)

    if not payroll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payroll not found"
        )

    payroll.status = PayrollStatus.PAID
    payroll.payment_date = payment_date

    await db.commit()
    await db.refresh(payroll)

    return payroll
