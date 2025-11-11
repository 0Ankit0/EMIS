"""Financial Aid Service for EMIS"""
from datetime import datetime, date
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload

from src.models.financial_aid import (
    Scholarship, FinancialAid, AidApplication,
    AidType, AidStatus
)
from src.lib.logging import get_logger

logger = get_logger(__name__)


class FinancialAidService:
    """Service for managing financial aid and scholarships"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # T222: Core financial aid service
    async def create_scholarship(
        self,
        scholarship_name: str,
        scholarship_code: str,
        aid_type: AidType,
        provider: str,
        amount: float,
        eligibility_criteria: str,
        academic_year: str,
        effective_from: date,
        **kwargs
    ) -> Scholarship:
        """Create new scholarship/grant program"""
        
        scholarship = Scholarship(
            scholarship_name=scholarship_name,
            scholarship_code=scholarship_code,
            aid_type=aid_type,
            provider=provider,
            amount=amount,
            eligibility_criteria=eligibility_criteria,
            academic_year=academic_year,
            effective_from=effective_from,
            **kwargs
        )
        
        self.db.add(scholarship)
        await self.db.commit()
        await self.db.refresh(scholarship)
        
        logger.info(f"Created scholarship: {scholarship_name} ({scholarship_code})")
        
        return scholarship
    
    async def get_active_scholarships(
        self,
        academic_year: Optional[str] = None,
        aid_type: Optional[AidType] = None
    ) -> List[Scholarship]:
        """Get all active scholarships"""
        query = select(Scholarship).where(Scholarship.is_active == True)
        
        if academic_year:
            query = query.where(Scholarship.academic_year == academic_year)
        
        if aid_type:
            query = query.where(Scholarship.aid_type == aid_type)
        
        today = date.today()
        query = query.where(
            and_(
                Scholarship.effective_from <= today,
                or_(
                    Scholarship.effective_to == None,
                    Scholarship.effective_to >= today
                )
            )
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def apply_for_scholarship(
        self,
        scholarship_id: int,
        student_id: int,
        academic_year: str,
        semester: Optional[int] = None
    ) -> FinancialAid:
        """Submit scholarship application"""
        
        # Check scholarship exists and is active
        scholarship = await self.get_scholarship_by_id(scholarship_id)
        if not scholarship or not scholarship.is_active:
            raise ValueError("Scholarship not found or inactive")
        
        # Check if application period is open
        today = date.today()
        if scholarship.application_start_date and today < scholarship.application_start_date:
            raise ValueError("Application period has not started")
        
        if scholarship.application_end_date and today > scholarship.application_end_date:
            raise ValueError("Application period has ended")
        
        # Check if student already applied
        existing = await self.get_student_aid_application(student_id, scholarship_id, academic_year)
        if existing:
            raise ValueError("Student has already applied for this scholarship")
        
        # Generate application number
        app_number = await self.generate_application_number(scholarship.scholarship_code, academic_year)
        
        # Create application
        aid = FinancialAid(
            application_number=app_number,
            scholarship_id=scholarship_id,
            student_id=student_id,
            academic_year=academic_year,
            semester=semester,
            requested_amount=scholarship.amount,
            status=AidStatus.DRAFT
        )
        
        self.db.add(aid)
        await self.db.commit()
        await self.db.refresh(aid)
        
        logger.info(f"Created financial aid application {app_number} for student {student_id}")
        
        return aid
    
    async def generate_application_number(self, scholarship_code: str, academic_year: str) -> str:
        """Generate unique application number"""
        year_short = academic_year.split('-')[0][2:]  # Get last 2 digits of first year
        
        # Get count for this scholarship and year
        result = await self.db.execute(
            select(func.count(FinancialAid.id)).where(
                and_(
                    FinancialAid.application_number.like(f"{scholarship_code}{year_short}%"),
                    FinancialAid.academic_year == academic_year
                )
            )
        )
        count = result.scalar() or 0
        sequence = str(count + 1).zfill(4)
        
        return f"{scholarship_code}{year_short}{sequence}"
    
    async def get_scholarship_by_id(self, scholarship_id: int) -> Optional[Scholarship]:
        """Get scholarship by ID"""
        result = await self.db.execute(
            select(Scholarship).where(Scholarship.id == scholarship_id)
        )
        return result.scalar_one_or_none()
    
    async def get_student_aid_application(
        self,
        student_id: int,
        scholarship_id: int,
        academic_year: str
    ) -> Optional[FinancialAid]:
        """Check if student already applied"""
        result = await self.db.execute(
            select(FinancialAid).where(
                and_(
                    FinancialAid.student_id == student_id,
                    FinancialAid.scholarship_id == scholarship_id,
                    FinancialAid.academic_year == academic_year
                )
            )
        )
        return result.scalar_one_or_none()
    
    # T223: Eligibility verification
    async def verify_eligibility(
        self,
        aid_id: int,
        student_percentage: float,
        family_income: float,
        category: str
    ) -> bool:
        """Verify student eligibility for financial aid"""
        
        aid = await self.get_aid_by_id(aid_id)
        if not aid:
            raise ValueError("Financial aid application not found")
        
        scholarship = aid.scholarship
        
        # Check minimum percentage
        if scholarship.minimum_percentage and student_percentage < scholarship.minimum_percentage:
            aid.is_eligible = False
            aid.review_comments = f"Does not meet minimum percentage requirement ({scholarship.minimum_percentage}%)"
            await self.db.commit()
            return False
        
        # Check family income limit
        if scholarship.family_income_limit and family_income > scholarship.family_income_limit:
            aid.is_eligible = False
            aid.review_comments = f"Family income exceeds limit (₹{scholarship.family_income_limit})"
            await self.db.commit()
            return False
        
        # Check category eligibility
        if scholarship.category_eligibility:
            eligible_categories = [c.strip() for c in scholarship.category_eligibility.split(',')]
            if category not in eligible_categories:
                aid.is_eligible = False
                aid.review_comments = f"Category {category} not eligible for this scholarship"
                await self.db.commit()
                return False
        
        # Store verified details
        aid.verified_percentage = student_percentage
        aid.verified_family_income = family_income
        aid.verified_category = category
        aid.is_eligible = True
        aid.status = AidStatus.UNDER_REVIEW
        aid.review_comments = "Eligibility criteria met"
        
        await self.db.commit()
        
        logger.info(f"Verified eligibility for aid {aid.application_number}: Eligible")
        
        return True
    
    async def approve_aid(
        self,
        aid_id: int,
        approver_id: int,
        approved_amount: Optional[float] = None,
        comments: Optional[str] = None
    ) -> FinancialAid:
        """Approve financial aid application"""
        
        aid = await self.get_aid_by_id(aid_id)
        if not aid:
            raise ValueError("Financial aid application not found")
        
        if not aid.is_eligible:
            raise ValueError("Cannot approve ineligible application")
        
        # Update scholarship beneficiary count
        scholarship = aid.scholarship
        if scholarship.max_students and scholarship.current_beneficiaries >= scholarship.max_students:
            raise ValueError("Maximum beneficiaries limit reached for this scholarship")
        
        aid.status = AidStatus.APPROVED
        aid.approved_amount = approved_amount or aid.requested_amount
        aid.approved_by = approver_id
        aid.approval_date = datetime.utcnow()
        aid.approval_comments = comments
        
        # Increment beneficiary count
        scholarship.current_beneficiaries += 1
        
        await self.db.commit()
        await self.db.refresh(aid)
        
        logger.info(f"Approved financial aid {aid.application_number} for ₹{aid.approved_amount}")
        
        return aid
    
    async def reject_aid(
        self,
        aid_id: int,
        rejector_id: int,
        reason: str
    ) -> FinancialAid:
        """Reject financial aid application"""
        
        aid = await self.get_aid_by_id(aid_id)
        if not aid:
            raise ValueError("Financial aid application not found")
        
        aid.status = AidStatus.REJECTED
        aid.approved_by = rejector_id
        aid.approval_date = datetime.utcnow()
        aid.rejection_reason = reason
        
        await self.db.commit()
        await self.db.refresh(aid)
        
        logger.info(f"Rejected financial aid {aid.application_number}: {reason}")
        
        return aid
    
    # T224: Aid disbursement workflow
    async def disburse_aid(
        self,
        aid_id: int,
        disbursement_method: str,
        disbursement_reference: Optional[str] = None
    ) -> FinancialAid:
        """Disburse approved financial aid"""
        
        aid = await self.get_aid_by_id(aid_id)
        if not aid:
            raise ValueError("Financial aid application not found")
        
        if aid.status != AidStatus.APPROVED:
            raise ValueError("Only approved aid can be disbursed")
        
        aid.disbursed_amount = aid.approved_amount
        aid.disbursement_date = datetime.utcnow()
        aid.disbursement_method = disbursement_method
        aid.disbursement_reference = disbursement_reference
        aid.status = AidStatus.DISBURSED
        
        await self.db.commit()
        await self.db.refresh(aid)
        
        logger.info(f"Disbursed aid {aid.application_number}: ₹{aid.disbursed_amount}")
        
        return aid
    
    # T225: Integrate with billing for aid adjustment
    async def adjust_aid_in_bill(
        self,
        aid_id: int,
        bill_id: int
    ) -> FinancialAid:
        """Adjust financial aid amount in student's bill"""
        from src.services.billing_service import BillingService
        from src.models.billing import BillItem
        
        aid = await self.get_aid_by_id(aid_id)
        if not aid:
            raise ValueError("Financial aid application not found")
        
        if aid.status != AidStatus.APPROVED:
            raise ValueError("Only approved aid can be adjusted")
        
        billing_service = BillingService(self.db)
        bill = await billing_service.get_bill_by_id(bill_id)
        
        if not bill:
            raise ValueError("Bill not found")
        
        if bill.student_id != aid.student_id:
            raise ValueError("Bill does not belong to the aid recipient")
        
        # Add negative line item for aid adjustment
        aid_item = BillItem(
            bill_id=bill_id,
            item_name=f"{aid.scholarship.scholarship_name} - Aid Adjustment",
            description=f"Financial aid applied (Application: {aid.application_number})",
            quantity=1.0,
            unit_price=-aid.approved_amount,
            amount=-aid.approved_amount,
            category="FINANCIAL_AID"
        )
        self.db.add(aid_item)
        
        # Update bill totals
        bill.discount_amount += aid.approved_amount
        bill.total_amount -= aid.approved_amount
        bill.amount_due = max(0, bill.total_amount - bill.amount_paid)
        
        # Update aid record
        aid.adjusted_bill_id = bill_id
        aid.adjustment_amount = aid.approved_amount
        aid.disbursement_method = "adjustment_in_fee"
        aid.disbursement_date = datetime.utcnow()
        aid.status = AidStatus.DISBURSED
        
        await self.db.commit()
        await self.db.refresh(aid)
        
        logger.info(f"Adjusted ₹{aid.approved_amount} from bill {bill.bill_number} for aid {aid.application_number}")
        
        return aid
    
    async def get_aid_by_id(self, aid_id: int) -> Optional[FinancialAid]:
        """Get financial aid by ID"""
        result = await self.db.execute(
            select(FinancialAid)
            .options(selectinload(FinancialAid.scholarship))
            .where(FinancialAid.id == aid_id)
        )
        return result.scalar_one_or_none()
    
    async def get_student_aids(
        self,
        student_id: int,
        status: Optional[AidStatus] = None
    ) -> List[FinancialAid]:
        """Get all financial aids for a student"""
        query = select(FinancialAid).where(FinancialAid.student_id == student_id)
        
        if status:
            query = query.where(FinancialAid.status == status)
        
        query = query.order_by(FinancialAid.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_pending_aids(self) -> List[FinancialAid]:
        """Get all pending aid applications for review"""
        result = await self.db.execute(
            select(FinancialAid)
            .options(selectinload(FinancialAid.scholarship), selectinload(FinancialAid.student))
            .where(FinancialAid.status.in_([AidStatus.SUBMITTED, AidStatus.UNDER_REVIEW]))
            .order_by(FinancialAid.submitted_date)
        )
        return result.scalars().all()
    
    async def submit_aid_application(self, aid_id: int) -> FinancialAid:
        """Submit aid application for review"""
        aid = await self.get_aid_by_id(aid_id)
        if not aid:
            raise ValueError("Financial aid application not found")
        
        if aid.status != AidStatus.DRAFT:
            raise ValueError("Only draft applications can be submitted")
        
        aid.status = AidStatus.SUBMITTED
        aid.submitted_date = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(aid)
        
        logger.info(f"Submitted financial aid application {aid.application_number}")
        
        return aid
