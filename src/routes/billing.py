"""Billing API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date
from pydantic import BaseModel

from src.database import get_db
from src.services.billing_service import BillingService
from src.models.billing import BillType, BillStatus, PaymentMethod
from src.middleware.rbac import require_permissions
from src.lib.pdf_generator import PDFGenerator

router = APIRouter(prefix="/billing", tags=["billing"])


class BillItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: float = 1.0
    unit_price: float
    tax_percentage: float = 0.0
    discount_percentage: float = 0.0
    category: Optional[str] = None


class BillCreate(BaseModel):
    bill_type: BillType
    student_id: Optional[int] = None
    employee_id: Optional[int] = None
    items: List[BillItemCreate]
    due_date: Optional[date] = None
    academic_year: Optional[str] = None
    semester: Optional[int] = None
    description: Optional[str] = None


class BillResponse(BaseModel):
    id: int
    bill_number: str
    bill_type: BillType
    student_id: Optional[int]
    employee_id: Optional[int]
    bill_date: date
    due_date: date
    subtotal: float
    tax_amount: float
    discount_amount: float
    total_amount: float
    amount_paid: float
    amount_due: float
    status: BillStatus
    academic_year: Optional[str]
    semester: Optional[int]
    
    class Config:
        from_attributes = True


class PaymentRecord(BaseModel):
    amount: float
    payment_method: PaymentMethod
    transaction_id: Optional[str] = None


@router.post("/bills", response_model=BillResponse, status_code=status.HTTP_201_CREATED)
async def create_bill(
    bill_data: BillCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:create"]))
):
    """Create a new bill"""
    service = BillingService(db)
    
    # Convert items to dict
    items = [item.dict() for item in bill_data.items]
    
    bill = await service.create_bill(
        bill_type=bill_data.bill_type,
        student_id=bill_data.student_id,
        employee_id=bill_data.employee_id,
        items=items,
        due_date=bill_data.due_date,
        academic_year=bill_data.academic_year,
        semester=bill_data.semester,
        description=bill_data.description,
        generated_by=current_user.get("id")
    )
    
    return bill


@router.get("/bills/{bill_id}", response_model=BillResponse)
async def get_bill(
    bill_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:read"]))
):
    """Get bill by ID"""
    service = BillingService(db)
    bill = await service.get_bill_by_id(bill_id)
    
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bill {bill_id} not found"
        )
    
    return bill


@router.get("/bills/number/{bill_number}", response_model=BillResponse)
async def get_bill_by_number(
    bill_number: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:read"]))
):
    """Get bill by bill number"""
    service = BillingService(db)
    bill = await service.get_bill_by_number(bill_number)
    
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bill {bill_number} not found"
        )
    
    return bill


@router.get("/bills/student/{student_id}", response_model=List[BillResponse])
async def get_student_bills(
    student_id: int,
    status_filter: Optional[BillStatus] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:read"]))
):
    """Get all bills for a student"""
    service = BillingService(db)
    bills = await service.get_bills_by_student(student_id, status_filter)
    return bills


@router.get("/bills/overdue", response_model=List[BillResponse])
async def get_overdue_bills(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:read"]))
):
    """Get all overdue bills"""
    service = BillingService(db)
    bills = await service.get_overdue_bills()
    return bills


@router.post("/bills/{bill_id}/payment", response_model=BillResponse)
async def record_payment(
    bill_id: int,
    payment: PaymentRecord,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:payment"]))
):
    """Record payment for a bill"""
    service = BillingService(db)
    
    try:
        bill = await service.record_payment(
            bill_id=bill_id,
            amount=payment.amount,
            payment_method=payment.payment_method,
            transaction_id=payment.transaction_id
        )
        return bill
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/bills/{bill_id}/pdf")
async def download_bill_pdf(
    bill_id: int,
    download: bool = False,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:read"]))
):
    """Download or view bill as PDF
    
    Args:
        bill_id: ID of the bill
        download: If True, forces download. If False, displays inline (for print)
    
    Returns:
        PDF file as response
    """
    service = BillingService(db)
    bill = await service.get_bill_by_id(bill_id)
    
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bill {bill_id} not found"
        )
    
    # Generate PDF
    pdf_generator = PDFGenerator()
    filepath = f"/tmp/bill_{bill.bill_number}.pdf"
    
    pdf_generator.generate_bill_pdf(
        bill=bill,
        filepath=filepath,
        institution_name="Your Institution Name"
    )
    
    # Determine content disposition
    content_disposition = "attachment" if download else "inline"
    filename = f"Bill_{bill.bill_number}.pdf"
    
    return FileResponse(
        path=filepath,
        media_type="application/pdf",
        filename=filename,
        headers={
            "Content-Disposition": f'{content_disposition}; filename="{filename}"',
            "Cache-Control": "no-cache"
        }
    )


@router.get("/bills/{bill_id}/print")
async def print_bill(
    bill_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:read"]))
):
    """Generate print-optimized PDF for direct printing
    
    Returns PDF with inline disposition to open in browser print dialog
    """
    service = BillingService(db)
    bill = await service.get_bill_by_id(bill_id)
    
    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bill {bill_id} not found"
        )
    
    # Generate PDF
    pdf_generator = PDFGenerator()
    filepath = f"/tmp/bill_print_{bill.bill_number}.pdf"
    
    pdf_generator.generate_bill_pdf(
        bill=bill,
        filepath=filepath,
        institution_name="Your Institution Name"
    )
    
    filename = f"Print_Bill_{bill.bill_number}.pdf"
    
    return FileResponse(
        path=filepath,
        media_type="application/pdf",
        filename=filename,
        headers={
            "Content-Disposition": f'inline; filename="{filename}"',
            "Cache-Control": "no-cache",
            "X-Print-Preview": "true"
        }
    )


@router.post("/bills/{bill_id}/cancel", response_model=BillResponse)
async def cancel_bill(
    bill_id: int,
    reason: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:cancel"]))
):
    """Cancel a bill"""
    service = BillingService(db)
    
    try:
        bill = await service.cancel_bill(bill_id, reason)
        return bill
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# T214: Fee structure endpoints
class FeeStructureCreate(BaseModel):
    program_id: int
    academic_year: str
    semester: int
    template_name: str
    items: List[dict]


@router.post("/fee-structures", status_code=status.HTTP_201_CREATED)
async def create_fee_structure(
    fee_structure: FeeStructureCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:admin"]))
):
    """Create fee structure template (T207)"""
    service = BillingService(db)
    
    result = await service.create_fee_structure_template(
        program_id=fee_structure.program_id,
        academic_year=fee_structure.academic_year,
        semester=fee_structure.semester,
        template_name=fee_structure.template_name,
        items=fee_structure.items
    )
    
    return result


@router.post("/fee-structures/{template_id}/apply/{student_id}", response_model=BillResponse)
async def apply_fee_structure(
    template_id: int,
    student_id: int,
    due_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:create"]))
):
    """Apply fee structure template to student (T207)"""
    service = BillingService(db)
    
    try:
        bill = await service.apply_fee_structure_template(
            template_id=template_id,
            student_id=student_id,
            due_date=due_date
        )
        return bill
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# T215: Bulk bill generation endpoints
class BulkBillCreate(BaseModel):
    bill_type: BillType
    student_ids: List[int]
    items: List[dict]
    due_date: Optional[date] = None
    academic_year: Optional[str] = None
    semester: Optional[int] = None


@router.post("/bills/bulk-generate")
async def bulk_generate_bills(
    bulk_data: BulkBillCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:bulk_create"]))
):
    """Generate bills for multiple students (T210)"""
    service = BillingService(db)
    
    result = await service.bulk_generate_bills(
        bill_type=bulk_data.bill_type,
        student_ids=bulk_data.student_ids,
        items=bulk_data.items,
        due_date=bulk_data.due_date,
        academic_year=bulk_data.academic_year,
        semester=bulk_data.semester
    )
    
    return result


# T216: Payment processing endpoints (already exists above, but add late fee management)
@router.post("/bills/apply-late-fees")
async def apply_late_fees(
    grace_days: int = 7,
    late_fee_percentage: float = 5.0,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:admin"]))
):
    """Apply late fees to overdue bills (T208)"""
    service = BillingService(db)
    
    count = await service.apply_late_fees(grace_days, late_fee_percentage)
    
    return {
        "message": f"Applied late fees to {count} bills",
        "count": count
    }


# T209: Installment management endpoints
class InstallmentPlanCreate(BaseModel):
    num_installments: int
    first_installment_date: date


@router.post("/bills/{bill_id}/installments")
async def create_installment_plan(
    bill_id: int,
    plan: InstallmentPlanCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:create"]))
):
    """Create installment plan for bill (T209)"""
    service = BillingService(db)
    
    try:
        installments = await service.create_installment_plan(
            bill_id=bill_id,
            num_installments=plan.num_installments,
            first_installment_date=plan.first_installment_date
        )
        return {"installments": installments}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


class InstallmentPayment(BaseModel):
    amount: float
    payment_method: PaymentMethod


@router.post("/bills/{bill_id}/installments/{installment_number}/pay", response_model=BillResponse)
async def pay_installment(
    bill_id: int,
    installment_number: int,
    payment: InstallmentPayment,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:payment"]))
):
    """Record payment for specific installment (T209)"""
    service = BillingService(db)
    
    try:
        bill = await service.record_installment_payment(
            bill_id=bill_id,
            installment_number=installment_number,
            amount=payment.amount,
            payment_method=payment.payment_method
        )
        return bill
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# T217: Bill printing endpoint (already exists above as /bills/{bill_id}/print)

# T213: Email bill functionality
class EmailBillRequest(BaseModel):
    recipient_email: str
    include_pdf: bool = True


@router.post("/bills/{bill_id}/email")
async def email_bill(
    bill_id: int,
    email_request: EmailBillRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["billing:send"]))
):
    """Email bill to recipient (T213)"""
    service = BillingService(db)
    
    try:
        success = await service.email_bill(
            bill_id=bill_id,
            recipient_email=email_request.recipient_email,
            include_pdf=email_request.include_pdf
        )
        
        if success:
            return {"message": "Bill emailed successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send email"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
