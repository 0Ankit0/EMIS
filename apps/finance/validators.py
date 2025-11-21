"""Finance Validators"""
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal


def validate_amount_positive(value):
    """Validate that amount is positive"""
    if value <= 0:
        raise ValidationError('Amount must be greater than zero')


def validate_future_date(value):
    """Validate that date is not in the future"""
    if value > timezone.now().date():
        raise ValidationError('Date cannot be in the future')


def validate_date_range(start_date, end_date):
    """Validate that end_date is after start_date"""
    if end_date < start_date:
        raise ValidationError('End date must be after start date')


def validate_percentage(value):
    """Validate percentage is between 0 and 100"""
    if not (0 <= value <= 100):
        raise ValidationError('Percentage must be between 0 and 100')


def validate_invoice_payment(invoice, payment_amount):
    """Validate payment against invoice"""
    payment_amount = Decimal(str(payment_amount))
    
    if payment_amount <= 0:
        raise ValidationError('Payment amount must be greater than zero')
    
    outstanding = invoice.balance
    if payment_amount > outstanding:
        raise ValidationError(
            f'Payment amount ({payment_amount}) cannot exceed outstanding balance ({outstanding})'
        )
    
    return True


def validate_budget_allocation(budget, allocations):
    """Validate that budget allocations don't exceed total budget"""
    total_allocated = sum(Decimal(str(a.get('allocated_amount', 0))) for a in allocations)
    
    if total_allocated > budget.total_allocated:
        raise ValidationError(
            f'Total allocations ({total_allocated}) exceed budget amount ({budget.total_allocated})'
        )
    
    return True


def validate_scholarship_slots(scholarship):
    """Validate scholarship slots"""
    if scholarship.filled_slots > scholarship.total_slots:
        raise ValidationError('Filled slots cannot exceed total slots')
    
    return True


def validate_fee_components(components):
    """Validate fee components structure"""
    if not isinstance(components, dict):
        raise ValidationError('Fee components must be a dictionary')
    
    for key, value in components.items():
        try:
            float_value = float(value)
            if float_value < 0:
                raise ValidationError(f'Component {key} cannot have negative value')
        except (ValueError, TypeError):
            raise ValidationError(f'Component {key} must have a numeric value')
    
    return True


def validate_installment_rules(rules):
    """Validate installment rules structure"""
    if not isinstance(rules, dict):
        raise ValidationError('Installment rules must be a dictionary')
    
    if rules.get('enabled'):
        count = rules.get('count')
        if not count or count < 1:
            raise ValidationError('Installment count must be at least 1')
        
        schedule = rules.get('schedule', [])
        if schedule and len(schedule) != count:
            raise ValidationError('Schedule length must match installment count')
    
    return True


def validate_expense_amount(expense):
    """Validate expense amounts"""
    if expense.amount < 0:
        raise ValidationError('Expense amount cannot be negative')
    
    if expense.tax_amount < 0:
        raise ValidationError('Tax amount cannot be negative')
    
    calculated_total = expense.amount + expense.tax_amount
    if abs(calculated_total - expense.total_amount) > Decimal('0.01'):
        raise ValidationError('Total amount does not match sum of amount and tax')
    
    return True


def validate_payment_date(payment_date, invoice_date):
    """Validate payment date is not before invoice date"""
    if payment_date < invoice_date:
        raise ValidationError('Payment date cannot be before invoice date')
    
    return True


def validate_transaction_id(transaction_id, payment_method):
    """Validate transaction ID is provided for certain payment methods"""
    online_methods = ['online', 'card', 'upi', 'bank_transfer']
    
    if payment_method in online_methods and not transaction_id:
        raise ValidationError(f'Transaction ID is required for {payment_method} payments')
    
    return True
