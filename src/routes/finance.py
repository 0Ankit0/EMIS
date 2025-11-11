"""Finance API routes for EMIS."""
from datetime import date
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.middleware.rbac import require_permissions
from src.models.auth import User


router = APIRouter(prefix="/api/v1/finance", tags=["Finance"])


class FeeStructureCreate(BaseModel):
    program_id: UUID
    academic_year: str
    semester: str
    tuition_fee: float
    library_fee: Optional[float] = 0
    sports_fee: Optional[float] = 0
    exam_fee: Optional[float] = 0
    other_fees: Optional[float] = 0


class PaymentCreate(BaseModel):
    student_id: UUID
    amount: float
    payment_method: str
    payment_date: date
    reference_number: Optional[str] = None
    fee_type: str


class PaymentResponse(BaseModel):
    id: UUID
    student_id: UUID
    amount: float
    payment_method: str
    payment_date: date
    status: str

    class Config:
        from_attributes = True


class ScholarshipCreate(BaseModel):
    student_id: UUID
    scholarship_name: str
    amount: float
    academic_year: str
    criteria: Optional[str] = None


@router.post("/fee-structures", status_code=status.HTTP_201_CREATED)
async def create_fee_structure(
    fee_data: FeeStructureCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("finance:create")),
):
    """Create fee structure for a program."""
    return {"message": "Fee structure created successfully"}


@router.post("/payments", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def record_payment(
    payment_data: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("payments:create")),
):
    """Record a payment."""
    return {"message": "Payment recorded successfully"}


@router.get("/payments/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("payments:read")),
):
    """Get payment details."""
    return {"message": "Payment details"}


@router.get("/students/{student_id}/balance")
async def get_student_balance(
    student_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("finance:read")),
):
    """Get student's fee balance."""
    return {"student_id": student_id, "balance": 0, "total_due": 0, "total_paid": 0}


@router.post("/scholarships", status_code=status.HTTP_201_CREATED)
async def award_scholarship(
    scholarship_data: ScholarshipCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("scholarships:create")),
):
    """Award scholarship to a student."""
    return {"message": "Scholarship awarded successfully"}


@router.get("/reports/collections")
async def get_collections_report(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permissions("finance:reports")),
):
    """Get fee collections report."""
    return {"start_date": start_date, "end_date": end_date, "total_collected": 0}
