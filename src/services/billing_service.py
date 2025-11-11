"""Billing Service for EMIS"""
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload

from src.models.billing import (
    Bill, BillItem, BillType, BillStatus, PaymentMethod,
    MaintenanceFee, EmergencyExpense
)
from src.models.accounting import JournalEntry, TransactionType
from src.lib.logging import get_logger

logger = get_logger(__name__)


class BillingService:
    """Service for managing billing operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def generate_bill_number(self, bill_type: BillType) -> str:
        """Generate unique bill number"""
        prefix = {
            BillType.TUITION_FEE: "TF",
            BillType.ADMISSION_FEE: "AF",
            BillType.EXAM_FEE: "EF",
            BillType.LIBRARY_FEE: "LF",
            BillType.MAINTENANCE_FEE: "MF",
            BillType.FINE: "FN",
        }.get(bill_type, "BL")
        
        today = date.today()
        year_month = today.strftime("%Y%m")
        
        # Get count for today
        result = await self.db.execute(
            select(func.count(Bill.id)).where(
                and_(
                    Bill.bill_number.like(f"{prefix}{year_month}%"),
                    Bill.bill_type == bill_type
                )
            )
        )
        count = result.scalar() or 0
        sequence = str(count + 1).zfill(4)
        
        return f"{prefix}{year_month}{sequence}"
    
    async def create_bill(
        self,
        bill_type: BillType,
        student_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        items: List[Dict] = None,
        due_date: Optional[date] = None,
        academic_year: Optional[str] = None,
        semester: Optional[int] = None,
        description: Optional[str] = None,
        generated_by: Optional[int] = None
    ) -> Bill:
        """Create a new bill"""
        
        # Generate bill number
        bill_number = await self.generate_bill_number(bill_type)
        
        # Calculate due date if not provided
        if not due_date:
            due_date = date.today() + timedelta(days=30)
        
        # Create bill
        bill = Bill(
            bill_number=bill_number,
            bill_type=bill_type,
            student_id=student_id,
            employee_id=employee_id,
            bill_date=date.today(),
            due_date=due_date,
            academic_year=academic_year,
            semester=semester,
            description=description,
            generated_by=generated_by,
            status=BillStatus.DRAFT
        )
        
        # Add items
        subtotal = 0.0
        tax_total = 0.0
        
        if items:
            for item_data in items:
                item = BillItem(
                    item_name=item_data['name'],
                    description=item_data.get('description'),
                    quantity=item_data.get('quantity', 1.0),
                    unit_price=item_data['unit_price'],
                    amount=item_data['quantity'] * item_data['unit_price'],
                    tax_percentage=item_data.get('tax_percentage', 0.0),
                    discount_percentage=item_data.get('discount_percentage', 0.0),
                    category=item_data.get('category')
                )
                bill.items.append(item)
                subtotal += item.amount
                tax_total += (item.amount * item.tax_percentage / 100)
        
        bill.subtotal = subtotal
        bill.tax_amount = tax_total
        bill.total_amount = subtotal + tax_total
        bill.amount_due = bill.total_amount
        
        self.db.add(bill)
        await self.db.commit()
        await self.db.refresh(bill)
        
        logger.info(f"Created bill {bill.bill_number} for {'student' if student_id else 'employee'} {student_id or employee_id}")
        
        return bill
    
    async def get_bill_by_id(self, bill_id: int) -> Optional[Bill]:
        """Get bill by ID"""
        result = await self.db.execute(
            select(Bill)
            .options(selectinload(Bill.items))
            .where(Bill.id == bill_id)
        )
        return result.scalar_one_or_none()
    
    async def get_bill_by_number(self, bill_number: str) -> Optional[Bill]:
        """Get bill by number"""
        result = await self.db.execute(
            select(Bill)
            .options(selectinload(Bill.items))
            .where(Bill.bill_number == bill_number)
        )
        return result.scalar_one_or_none()
    
    async def get_bills_by_student(
        self,
        student_id: int,
        status: Optional[BillStatus] = None
    ) -> List[Bill]:
        """Get all bills for a student"""
        query = select(Bill).where(Bill.student_id == student_id)
        
        if status:
            query = query.where(Bill.status == status)
        
        query = query.order_by(Bill.bill_date.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_overdue_bills(self) -> List[Bill]:
        """Get all overdue bills"""
        today = date.today()
        result = await self.db.execute(
            select(Bill).where(
                and_(
                    Bill.due_date < today,
                    Bill.status.in_([BillStatus.GENERATED, BillStatus.SENT, BillStatus.PARTIALLY_PAID])
                )
            ).order_by(Bill.due_date)
        )
        return result.scalars().all()
    
    async def record_payment(
        self,
        bill_id: int,
        amount: float,
        payment_method: PaymentMethod,
        transaction_id: Optional[str] = None
    ) -> Bill:
        """Record payment for a bill"""
        bill = await self.get_bill_by_id(bill_id)
        if not bill:
            raise ValueError(f"Bill {bill_id} not found")
        
        bill.amount_paid += amount
        bill.amount_due = bill.total_amount - bill.amount_paid
        bill.payment_method = payment_method
        bill.transaction_id = transaction_id
        bill.payment_date = datetime.utcnow()
        
        if bill.amount_due <= 0:
            bill.status = BillStatus.PAID
        elif bill.amount_paid > 0:
            bill.status = BillStatus.PARTIALLY_PAID
        
        await self.db.commit()
        await self.db.refresh(bill)
        
        # Create journal entry for payment
        await self._create_payment_journal_entry(bill, amount)
        
        logger.info(f"Recorded payment of {amount} for bill {bill.bill_number}")
        
        return bill
    
    async def _create_payment_journal_entry(self, bill: Bill, amount: float):
        """Create journal entry for payment"""
        from src.services.accounting_service import AccountingService
        
        accounting_service = AccountingService(self.db)
        
        # Credit entry for income
        await accounting_service.create_journal_entry(
            transaction_type=TransactionType.CREDIT,
            account_code="4000",  # Revenue account
            account_name=f"{bill.bill_type.value.replace('_', ' ').title()} Income",
            debit_amount=0.0,
            credit_amount=amount,
            description=f"Payment received for bill {bill.bill_number}",
            source_type="bill_payment",
            source_id=bill.id
        )
    
    async def generate_fee_bills_for_semester(
        self,
        academic_year: str,
        semester: int,
        program_id: Optional[int] = None
    ) -> int:
        """Generate fee bills for all students in a semester"""
        # This would query students and generate bills
        # Implementation depends on fee structure setup
        count = 0
        # ... implementation
        return count
    
    async def apply_maintenance_fee(
        self,
        maintenance_fee_id: int,
        student_ids: List[int] = None,
        academic_year: Optional[str] = None
    ) -> List[Bill]:
        """Apply maintenance fee to students"""
        result = await self.db.execute(
            select(MaintenanceFee).where(MaintenanceFee.id == maintenance_fee_id)
        )
        fee = result.scalar_one_or_none()
        
        if not fee:
            raise ValueError(f"Maintenance fee {maintenance_fee_id} not found")
        
        bills = []
        
        for student_id in (student_ids or []):
            bill = await self.create_bill(
                bill_type=BillType.MAINTENANCE_FEE,
                student_id=student_id,
                items=[{
                    'name': fee.fee_name,
                    'description': fee.description,
                    'quantity': 1,
                    'unit_price': fee.amount
                }],
                academic_year=academic_year or fee.academic_year
            )
            bills.append(bill)
        
        logger.info(f"Applied maintenance fee to {len(bills)} students")
        
        return bills
    
    async def cancel_bill(self, bill_id: int, reason: Optional[str] = None) -> Bill:
        """Cancel a bill"""
        bill = await self.get_bill_by_id(bill_id)
        if not bill:
            raise ValueError(f"Bill {bill_id} not found")
        
        if bill.status == BillStatus.PAID:
            raise ValueError("Cannot cancel a paid bill")
        
        bill.status = BillStatus.CANCELLED
        if reason:
            bill.notes = f"Cancelled: {reason}"
        
        await self.db.commit()
        await self.db.refresh(bill)
        
        logger.info(f"Cancelled bill {bill.bill_number}")
        
        return bill
    
    # T207: Fee structure templates
    async def create_fee_structure_template(
        self,
        program_id: int,
        academic_year: str,
        semester: int,
        template_name: str,
        items: List[Dict]
    ) -> Dict:
        """Create reusable fee structure template"""
        from src.models.fee import FeeStructure
        
        fee_structure = FeeStructure(
            program_id=program_id,
            academic_year=academic_year,
            semester=semester,
            name=template_name,
            is_active=True
        )
        
        total_amount = 0.0
        for item in items:
            total_amount += item.get('amount', 0.0)
        
        fee_structure.total_amount = total_amount
        fee_structure.items = items  # Store as JSON
        
        self.db.add(fee_structure)
        await self.db.commit()
        await self.db.refresh(fee_structure)
        
        logger.info(f"Created fee structure template '{template_name}' for program {program_id}")
        
        return {
            'id': fee_structure.id,
            'name': template_name,
            'total_amount': total_amount,
            'items': items
        }
    
    async def apply_fee_structure_template(
        self,
        template_id: int,
        student_id: int,
        due_date: Optional[date] = None
    ) -> Bill:
        """Apply fee structure template to create bill"""
        from src.models.fee import FeeStructure
        
        result = await self.db.execute(
            select(FeeStructure).where(FeeStructure.id == template_id)
        )
        template = result.scalar_one_or_none()
        
        if not template:
            raise ValueError(f"Fee structure template {template_id} not found")
        
        bill = await self.create_bill(
            bill_type=BillType.TUITION_FEE,
            student_id=student_id,
            items=template.items,
            due_date=due_date,
            academic_year=template.academic_year,
            semester=template.semester,
            description=f"Applied from template: {template.name}"
        )
        
        return bill
    
    # T208: Late fee calculation
    async def calculate_late_fee(
        self,
        bill: Bill,
        late_fee_percentage: float = 5.0,
        grace_days: int = 7
    ) -> float:
        """Calculate late fee for overdue bill"""
        if bill.status == BillStatus.PAID:
            return 0.0
        
        today = date.today()
        if bill.due_date >= today:
            return 0.0
        
        days_overdue = (today - bill.due_date).days
        
        if days_overdue <= grace_days:
            return 0.0
        
        # Calculate late fee
        late_fee = (bill.amount_due * late_fee_percentage) / 100
        
        # Cap at 20% of original amount
        max_late_fee = bill.total_amount * 0.20
        late_fee = min(late_fee, max_late_fee)
        
        return round(late_fee, 2)
    
    async def apply_late_fees(self, grace_days: int = 7, late_fee_percentage: float = 5.0) -> int:
        """Apply late fees to all overdue bills"""
        overdue_bills = await self.get_overdue_bills()
        count = 0
        
        for bill in overdue_bills:
            late_fee = await self.calculate_late_fee(bill, late_fee_percentage, grace_days)
            
            if late_fee > 0 and not bill.late_fee_applied:
                # Add late fee as bill item
                late_fee_item = BillItem(
                    bill_id=bill.id,
                    item_name="Late Payment Fee",
                    description=f"Late fee for {(date.today() - bill.due_date).days} days overdue",
                    quantity=1.0,
                    unit_price=late_fee,
                    amount=late_fee,
                    category="LATE_FEE"
                )
                self.db.add(late_fee_item)
                
                # Update bill totals
                bill.total_amount += late_fee
                bill.amount_due += late_fee
                bill.late_fee_applied = True
                
                count += 1
        
        await self.db.commit()
        logger.info(f"Applied late fees to {count} bills")
        
        return count
    
    # T209: Installment management
    async def create_installment_plan(
        self,
        bill_id: int,
        num_installments: int,
        first_installment_date: date
    ) -> List[Dict]:
        """Create installment plan for a bill"""
        bill = await self.get_bill_by_id(bill_id)
        if not bill:
            raise ValueError(f"Bill {bill_id} not found")
        
        if bill.status == BillStatus.PAID:
            raise ValueError("Cannot create installment plan for paid bill")
        
        installment_amount = round(bill.total_amount / num_installments, 2)
        installments = []
        
        for i in range(num_installments):
            installment_date = first_installment_date + timedelta(days=30 * i)
            
            # Adjust last installment to account for rounding
            amount = installment_amount
            if i == num_installments - 1:
                amount = bill.total_amount - (installment_amount * (num_installments - 1))
            
            installments.append({
                'installment_number': i + 1,
                'amount': amount,
                'due_date': installment_date,
                'status': 'pending'
            })
        
        # Store installments in bill metadata
        bill.installments = installments
        bill.has_installments = True
        await self.db.commit()
        
        logger.info(f"Created {num_installments} installment plan for bill {bill.bill_number}")
        
        return installments
    
    async def record_installment_payment(
        self,
        bill_id: int,
        installment_number: int,
        amount: float,
        payment_method: PaymentMethod
    ) -> Bill:
        """Record payment for specific installment"""
        bill = await self.get_bill_by_id(bill_id)
        if not bill or not bill.has_installments:
            raise ValueError("Bill not found or has no installment plan")
        
        installments = bill.installments or []
        
        for installment in installments:
            if installment['installment_number'] == installment_number:
                if installment['status'] == 'paid':
                    raise ValueError(f"Installment {installment_number} already paid")
                
                installment['status'] = 'paid'
                installment['paid_date'] = date.today().isoformat()
                break
        
        bill.installments = installments
        
        # Record payment
        await self.record_payment(bill_id, amount, payment_method)
        
        return bill
    
    # T210: Bulk bill generation
    async def bulk_generate_bills(
        self,
        bill_type: BillType,
        student_ids: List[int],
        items: List[Dict],
        due_date: Optional[date] = None,
        academic_year: Optional[str] = None,
        semester: Optional[int] = None,
        batch_size: int = 100
    ) -> Dict:
        """Generate bills for multiple students in batches"""
        total_bills = []
        errors = []
        
        for i in range(0, len(student_ids), batch_size):
            batch = student_ids[i:i + batch_size]
            
            for student_id in batch:
                try:
                    bill = await self.create_bill(
                        bill_type=bill_type,
                        student_id=student_id,
                        items=items,
                        due_date=due_date,
                        academic_year=academic_year,
                        semester=semester
                    )
                    total_bills.append(bill)
                except Exception as e:
                    errors.append({
                        'student_id': student_id,
                        'error': str(e)
                    })
                    logger.error(f"Failed to generate bill for student {student_id}: {e}")
        
        logger.info(f"Bulk generated {len(total_bills)} bills, {len(errors)} errors")
        
        return {
            'success_count': len(total_bills),
            'error_count': len(errors),
            'bills': total_bills,
            'errors': errors
        }
    
    # T213: Email bill functionality
    async def email_bill(
        self,
        bill_id: int,
        recipient_email: str,
        include_pdf: bool = True
    ) -> bool:
        """Send bill via email"""
        from src.lib.email import send_email
        from src.lib.pdf_generator import generate_bill_pdf
        
        bill = await self.get_bill_by_id(bill_id)
        if not bill:
            raise ValueError(f"Bill {bill_id} not found")
        
        # Generate PDF if requested
        pdf_data = None
        if include_pdf:
            pdf_data = generate_bill_pdf(bill)
        
        # Prepare email content
        subject = f"Bill {bill.bill_number} - {bill.bill_type.value.replace('_', ' ').title()}"
        
        body = f"""
Dear Student/Parent,

This is to inform you that a new bill has been generated.

Bill Number: {bill.bill_number}
Bill Date: {bill.bill_date}
Due Date: {bill.due_date}
Total Amount: ₹{bill.total_amount:,.2f}
Amount Due: ₹{bill.amount_due:,.2f}

Please make the payment before the due date to avoid late fees.

{f"Academic Year: {bill.academic_year}" if bill.academic_year else ""}
{f"Semester: {bill.semester}" if bill.semester else ""}

Thank you.
        """
        
        # Send email
        attachments = []
        if pdf_data:
            attachments.append({
                'filename': f'bill_{bill.bill_number}.pdf',
                'content': pdf_data,
                'mimetype': 'application/pdf'
            })
        
        success = await send_email(
            to_email=recipient_email,
            subject=subject,
            body=body,
            attachments=attachments
        )
        
        if success:
            bill.email_sent = True
            bill.email_sent_date = datetime.utcnow()
            bill.status = BillStatus.SENT
            await self.db.commit()
            logger.info(f"Emailed bill {bill.bill_number} to {recipient_email}")
        
        return success
    
    async def bulk_email_bills(
        self,
        bill_ids: List[int],
        get_recipient_email_func
    ) -> Dict:
        """Send bills to multiple recipients"""
        success_count = 0
        error_count = 0
        
        for bill_id in bill_ids:
            try:
                bill = await self.get_bill_by_id(bill_id)
                if not bill:
                    continue
                
                # Get recipient email (from student/parent record)
                recipient_email = await get_recipient_email_func(bill)
                
                if recipient_email:
                    success = await self.email_bill(bill_id, recipient_email)
                    if success:
                        success_count += 1
                    else:
                        error_count += 1
            except Exception as e:
                error_count += 1
                logger.error(f"Failed to email bill {bill_id}: {e}")
        
        return {
            'success_count': success_count,
            'error_count': error_count
        }
