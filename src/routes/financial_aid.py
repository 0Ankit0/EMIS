"""Financial Aid API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date
from pydantic import BaseModel

from src.database import get_db
from src.services.financial_aid_service import FinancialAidService
from src.models.financial_aid import AidType, AidStatus
from src.middleware.rbac import require_permissions

router = APIRouter(prefix="/financial-aid", tags=["financial-aid"])


class ScholarshipCreate(BaseModel):
    scholarship_name: str
    scholarship_code: str
    aid_type: AidType
    provider: str
    amount: float
    eligibility_criteria: str
    academic_year: str
    effective_from: date
    minimum_percentage: Optional[float] = None
    family_income_limit: Optional[float] = None
    category_eligibility: Optional[str] = None
    max_students: Optional[int] = None
    application_start_date: Optional[date] = None
    application_end_date: Optional[date] = None
    required_documents: Optional[str] = None


class ScholarshipResponse(BaseModel):
    id: int
    scholarship_name: str
    scholarship_code: str
    aid_type: AidType
    provider: str
    amount: float
    eligibility_criteria: str
    academic_year: str
    effective_from: date
    is_active: bool
    current_beneficiaries: int
    max_students: Optional[int]
    
    class Config:
        from_attributes = True


class AidApplicationCreate(BaseModel):
    scholarship_id: int
    student_id: int
    academic_year: str
    semester: Optional[int] = None


class AidResponse(BaseModel):
    id: int
    application_number: str
    scholarship_id: int
    student_id: int
    academic_year: str
    status: AidStatus
    requested_amount: float
    approved_amount: Optional[float]
    disbursed_amount: float
    is_eligible: bool
    
    class Config:
        from_attributes = True


class EligibilityVerification(BaseModel):
    student_percentage: float
    family_income: float
    category: str


class AidApproval(BaseModel):
    approved_amount: Optional[float] = None
    comments: Optional[str] = None


class AidRejection(BaseModel):
    reason: str


class DisbursementRequest(BaseModel):
    disbursement_method: str
    disbursement_reference: Optional[str] = None


class BillAdjustmentRequest(BaseModel):
    bill_id: int


# Scholarship Management
@router.post("/scholarships", response_model=ScholarshipResponse, status_code=status.HTTP_201_CREATED)
async def create_scholarship(
    scholarship_data: ScholarshipCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["financial_aid:admin"]))
):
    """Create new scholarship program"""
    service = FinancialAidService(db)
    
    scholarship = await service.create_scholarship(
        **scholarship_data.dict()
    )
    
    return scholarship


@router.get("/scholarships", response_model=List[ScholarshipResponse])
async def get_active_scholarships(
    academic_year: Optional[str] = None,
    aid_type: Optional[AidType] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["financial_aid:read"]))
):
    """Get all active scholarships"""
    service = FinancialAidService(db)
    
    scholarships = await service.get_active_scholarships(
        academic_year=academic_year,
        aid_type=aid_type
    )
    
    return scholarships


@router.get("/scholarships/{scholarship_id}", response_model=ScholarshipResponse)
async def get_scholarship(
    scholarship_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["financial_aid:read"]))
):
    """Get scholarship details"""
    service = FinancialAidService(db)
    
    scholarship = await service.get_scholarship_by_id(scholarship_id)
    
    if not scholarship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scholarship {scholarship_id} not found"
        )
    
    return scholarship


# Aid Applications
@router.post("/applications", response_model=AidResponse, status_code=status.HTTP_201_CREATED)
async def apply_for_scholarship(
    application_data: AidApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["financial_aid:apply"]))
):
    """Submit scholarship application"""
    service = FinancialAidService(db)
    
    try:
        aid = await service.apply_for_scholarship(
            scholarship_id=application_data.scholarship_id,
            student_id=application_data.student_id,
            academic_year=application_data.academic_year,
            semester=application_data.semester
        )
        return aid
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/applications/{aid_id}/submit", response_model=AidResponse)
async def submit_application(
    aid_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["financial_aid:apply"]))
):
    """Submit aid application for review (T223)"""
    service = FinancialAidService(db)
    
    try:
        aid = await service.submit_aid_application(aid_id)
        return aid
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/applications/{aid_id}", response_model=AidResponse)
async def get_aid_application(
    aid_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["financial_aid:read"]))
):
    """Get aid application details"""
    service = FinancialAidService(db)
    
    aid = await service.get_aid_by_id(aid_id)
    
    if not aid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aid application {aid_id} not found"
        )
    
    return aid


@router.get("/applications/student/{student_id}", response_model=List[AidResponse])
async def get_student_aids(
    student_id: int,
    status_filter: Optional[AidStatus] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["financial_aid:read"]))
):
    """Get all aid applications for a student"""
    service = FinancialAidService(db)
    
    aids = await service.get_student_aids(student_id, status_filter)
    
    return aids


@router.get("/applications/pending", response_model=List[AidResponse])
async def get_pending_applications(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["financial_aid:review"]))
):
    """Get all pending aid applications for review"""
    service = FinancialAidService(db)
    
    aids = await service.get_pending_aids()
    
    return aids


# Eligibility Verification (T223)
@router.post("/applications/{aid_id}/verify", response_model=AidResponse)
async def verify_eligibility(
    aid_id: int,
    verification_data: EligibilityVerification,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["financial_aid:verify"]))
):
    """Verify student eligibility for financial aid (T223)"""
    service = FinancialAidService(db)
    
    try:
        is_eligible = await service.verify_eligibility(
            aid_id=aid_id,
            student_percentage=verification_data.student_percentage,
            family_income=verification_data.family_income,
            category=verification_data.category
        )
        
        aid = await service.get_aid_by_id(aid_id)
        return aid
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# Approval Workflow
@router.post("/applications/{aid_id}/approve", response_model=AidResponse)
async def approve_aid(
    aid_id: int,
    approval_data: AidApproval,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["financial_aid:approve"]))
):
    """Approve financial aid application"""
    service = FinancialAidService(db)
    
    try:
        aid = await service.approve_aid(
            aid_id=aid_id,
            approver_id=current_user.get("id"),
            approved_amount=approval_data.approved_amount,
            comments=approval_data.comments
        )
        return aid
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/applications/{aid_id}/reject", response_model=AidResponse)
async def reject_aid(
    aid_id: int,
    rejection_data: AidRejection,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["financial_aid:approve"]))
):
    """Reject financial aid application"""
    service = FinancialAidService(db)
    
    try:
        aid = await service.reject_aid(
            aid_id=aid_id,
            rejector_id=current_user.get("id"),
            reason=rejection_data.reason
        )
        return aid
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# Disbursement (T224)
@router.post("/applications/{aid_id}/disburse", response_model=AidResponse)
async def disburse_aid(
    aid_id: int,
    disbursement_data: DisbursementRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["financial_aid:disburse"]))
):
    """Disburse approved financial aid (T224)"""
    service = FinancialAidService(db)
    
    try:
        aid = await service.disburse_aid(
            aid_id=aid_id,
            disbursement_method=disbursement_data.disbursement_method,
            disbursement_reference=disbursement_data.disbursement_reference
        )
        return aid
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# Bill Adjustment (T225)
@router.post("/applications/{aid_id}/adjust-in-bill", response_model=AidResponse)
async def adjust_aid_in_bill(
    aid_id: int,
    adjustment_data: BillAdjustmentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["financial_aid:disburse"]))
):
    """Adjust financial aid amount in student's bill (T225)"""
    service = FinancialAidService(db)
    
    try:
        aid = await service.adjust_aid_in_bill(
            aid_id=aid_id,
            bill_id=adjustment_data.bill_id
        )
        return aid
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
