"""Add billing, accounting, reports, and enhanced library tables

Revision ID: 003_billing_reporting
Revises: 002_add_new_tables
Create Date: 2025-11-09 14:30:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003_billing_reporting'
down_revision = '002_add_new_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create lost_book_settings table
    op.create_table(
        'lost_book_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('processing_fine_percentage', sa.Float(), nullable=False, default=20.0),
        sa.Column('minimum_processing_fine', sa.Float(), nullable=False, default=50.0),
        sa.Column('maximum_processing_fine', sa.Float(), nullable=False, default=500.0),
        sa.Column('grace_period_days', sa.Integer(), nullable=False, default=7),
        sa.Column('allow_waiver', sa.Boolean(), nullable=False, default=True),
        sa.Column('waiver_requires_approval', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create book_losses table
    op.create_table(
        'book_losses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('issue_id', sa.Integer(), nullable=False),
        sa.Column('member_id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('book_title', sa.String(length=500), nullable=False),
        sa.Column('book_isbn', sa.String(length=20), nullable=True),
        sa.Column('book_price', sa.Float(), nullable=False),
        sa.Column('reported_date', sa.DateTime(), nullable=False),
        sa.Column('loss_date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('book_replacement_cost', sa.Float(), nullable=False),
        sa.Column('processing_fine', sa.Float(), nullable=False, default=0.0),
        sa.Column('total_fine', sa.Float(), nullable=False),
        sa.Column('amount_paid', sa.Float(), nullable=False, default=0.0),
        sa.Column('is_paid', sa.Boolean(), nullable=False, default=False),
        sa.Column('paid_date', sa.DateTime(), nullable=True),
        sa.Column('investigation_notes', sa.Text(), nullable=True),
        sa.Column('resolution_notes', sa.Text(), nullable=True),
        sa.Column('reported_by', sa.Integer(), nullable=True),
        sa.Column('investigated_by', sa.Integer(), nullable=True),
        sa.Column('resolved_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_book_losses_id'), 'book_losses', ['id'], unique=False)
    
    # Create bills table
    op.create_table(
        'bills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('bill_number', sa.String(length=50), nullable=False, unique=True),
        sa.Column('student_id', sa.Integer(), nullable=True),
        sa.Column('employee_id', sa.Integer(), nullable=True),
        sa.Column('bill_type', sa.String(length=50), nullable=False),
        sa.Column('bill_date', sa.Date(), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('subtotal', sa.Float(), nullable=False, default=0.0),
        sa.Column('tax_amount', sa.Float(), nullable=False, default=0.0),
        sa.Column('discount_amount', sa.Float(), nullable=False, default=0.0),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('amount_paid', sa.Float(), nullable=False, default=0.0),
        sa.Column('amount_due', sa.Float(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('academic_year', sa.String(length=20), nullable=True),
        sa.Column('semester', sa.Integer(), nullable=True),
        sa.Column('quarter', sa.Integer(), nullable=True),
        sa.Column('payment_method', sa.String(length=50), nullable=True),
        sa.Column('transaction_id', sa.String(length=100), nullable=True),
        sa.Column('payment_date', sa.DateTime(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('terms_and_conditions', sa.Text(), nullable=True),
        sa.Column('pdf_path', sa.String(length=500), nullable=True),
        sa.Column('generated_by', sa.Integer(), nullable=True),
        sa.Column('sent_to_email', sa.String(length=255), nullable=True),
        sa.Column('sent_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bills_id'), 'bills', ['id'], unique=False)
    op.create_index(op.f('ix_bills_bill_number'), 'bills', ['bill_number'], unique=True)
    
    # Create bill_items table
    op.create_table(
        'bill_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('bill_id', sa.Integer(), nullable=False),
        sa.Column('item_name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('quantity', sa.Float(), nullable=False, default=1.0),
        sa.Column('unit_price', sa.Float(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('tax_percentage', sa.Float(), nullable=False, default=0.0),
        sa.Column('discount_percentage', sa.Float(), nullable=False, default=0.0),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['bill_id'], ['bills.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create maintenance_fees table
    op.create_table(
        'maintenance_fees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('fee_name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('applies_to_students', sa.Boolean(), nullable=False, default=True),
        sa.Column('applies_to_employees', sa.Boolean(), nullable=False, default=False),
        sa.Column('frequency', sa.String(length=50), nullable=False, default='yearly'),
        sa.Column('academic_year', sa.String(length=20), nullable=True),
        sa.Column('effective_from', sa.Date(), nullable=False),
        sa.Column('effective_to', sa.Date(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_mandatory', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create emergency_expenses table
    op.create_table(
        'emergency_expenses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('expense_title', sa.String(length=300), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('approved_amount', sa.Float(), nullable=True),
        sa.Column('priority', sa.String(length=20), nullable=False, default='medium'),
        sa.Column('is_emergency', sa.Boolean(), nullable=False, default=True),
        sa.Column('requested_by', sa.Integer(), nullable=True),
        sa.Column('approved_by', sa.Integer(), nullable=True),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.Column('is_paid', sa.Boolean(), nullable=False, default=False),
        sa.Column('paid_amount', sa.Float(), nullable=False, default=0.0),
        sa.Column('paid_date', sa.DateTime(), nullable=True),
        sa.Column('payment_method', sa.String(length=50), nullable=True),
        sa.Column('justification', sa.Text(), nullable=True),
        sa.Column('supporting_documents', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('journal_entry_id', sa.Integer(), nullable=True),
        sa.Column('expense_category_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create expense_categories table
    op.create_table(
        'expense_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False, unique=True),
        sa.Column('code', sa.String(length=50), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('monthly_budget', sa.Float(), nullable=True),
        sa.Column('quarterly_budget', sa.Float(), nullable=True),
        sa.Column('annual_budget', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['parent_id'], ['expense_categories.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_expense_categories_code'), 'expense_categories', ['code'], unique=True)
    
    # Create income_categories table
    op.create_table(
        'income_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False, unique=True),
        sa.Column('code', sa.String(length=50), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('monthly_target', sa.Float(), nullable=True),
        sa.Column('quarterly_target', sa.Float(), nullable=True),
        sa.Column('annual_target', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['parent_id'], ['income_categories.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_income_categories_code'), 'income_categories', ['code'], unique=True)
    
    # Create journal_entries table
    op.create_table(
        'journal_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entry_number', sa.String(length=50), nullable=False, unique=True),
        sa.Column('entry_date', sa.Date(), nullable=False),
        sa.Column('transaction_type', sa.String(length=20), nullable=False),
        sa.Column('account_code', sa.String(length=50), nullable=False),
        sa.Column('account_name', sa.String(length=200), nullable=False),
        sa.Column('debit_amount', sa.Float(), nullable=False, default=0.0),
        sa.Column('credit_amount', sa.Float(), nullable=False, default=0.0),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('reference_number', sa.String(length=100), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('category_type', sa.String(length=20), nullable=True),
        sa.Column('financial_year', sa.String(length=20), nullable=False),
        sa.Column('quarter', sa.Integer(), nullable=True),
        sa.Column('month', sa.Integer(), nullable=True),
        sa.Column('source_type', sa.String(length=50), nullable=True),
        sa.Column('source_id', sa.Integer(), nullable=True),
        sa.Column('is_approved', sa.Boolean(), nullable=False, default=False),
        sa.Column('approved_by', sa.Integer(), nullable=True),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_journal_entries_entry_number'), 'journal_entries', ['entry_number'], unique=True)
    op.create_index(op.f('ix_journal_entries_account_code'), 'journal_entries', ['account_code'], unique=False)
    
    # Create expenses table
    op.create_table(
        'expenses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('expense_number', sa.String(length=50), nullable=False, unique=True),
        sa.Column('expense_date', sa.Date(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=300), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('tax_amount', sa.Float(), nullable=False, default=0.0),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('payment_method', sa.String(length=50), nullable=True),
        sa.Column('payment_reference', sa.String(length=100), nullable=True),
        sa.Column('paid_to', sa.String(length=200), nullable=True),
        sa.Column('invoice_number', sa.String(length=100), nullable=True),
        sa.Column('supporting_documents', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('journal_entry_id', sa.Integer(), nullable=True),
        sa.Column('financial_year', sa.String(length=20), nullable=False),
        sa.Column('quarter', sa.Integer(), nullable=True),
        sa.Column('approved_by', sa.Integer(), nullable=True),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['expense_categories.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['journal_entry_id'], ['journal_entries.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_expenses_expense_number'), 'expenses', ['expense_number'], unique=True)
    
    # Create incomes table
    op.create_table(
        'incomes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('income_number', sa.String(length=50), nullable=False, unique=True),
        sa.Column('income_date', sa.Date(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=300), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('tax_amount', sa.Float(), nullable=False, default=0.0),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('payment_method', sa.String(length=50), nullable=True),
        sa.Column('payment_reference', sa.String(length=100), nullable=True),
        sa.Column('received_from', sa.String(length=200), nullable=True),
        sa.Column('receipt_number', sa.String(length=100), nullable=True),
        sa.Column('supporting_documents', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('journal_entry_id', sa.Integer(), nullable=True),
        sa.Column('financial_year', sa.String(length=20), nullable=False),
        sa.Column('quarter', sa.Integer(), nullable=True),
        sa.Column('recorded_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['income_categories.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['journal_entry_id'], ['journal_entries.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_incomes_income_number'), 'incomes', ['income_number'], unique=True)
    
    # Create quarterly_reports table
    op.create_table(
        'quarterly_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('report_number', sa.String(length=50), nullable=False, unique=True),
        sa.Column('report_type', sa.String(length=50), nullable=False),
        sa.Column('financial_year', sa.String(length=20), nullable=False),
        sa.Column('quarter', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('total_income', sa.Float(), nullable=False, default=0.0),
        sa.Column('total_expenses', sa.Float(), nullable=False, default=0.0),
        sa.Column('net_profit_loss', sa.Float(), nullable=False, default=0.0),
        sa.Column('tuition_fee_income', sa.Float(), default=0.0),
        sa.Column('admission_fee_income', sa.Float(), default=0.0),
        sa.Column('exam_fee_income', sa.Float(), default=0.0),
        sa.Column('library_fee_income', sa.Float(), default=0.0),
        sa.Column('other_fee_income', sa.Float(), default=0.0),
        sa.Column('miscellaneous_income', sa.Float(), default=0.0),
        sa.Column('salary_expenses', sa.Float(), default=0.0),
        sa.Column('maintenance_expenses', sa.Float(), default=0.0),
        sa.Column('utility_expenses', sa.Float(), default=0.0),
        sa.Column('infrastructure_expenses', sa.Float(), default=0.0),
        sa.Column('administrative_expenses', sa.Float(), default=0.0),
        sa.Column('emergency_expenses', sa.Float(), default=0.0),
        sa.Column('other_expenses', sa.Float(), default=0.0),
        sa.Column('student_count', sa.Integer(), default=0),
        sa.Column('employee_count', sa.Integer(), default=0),
        sa.Column('average_fee_per_student', sa.Float(), default=0.0),
        sa.Column('fee_collection_rate', sa.Float(), default=0.0),
        sa.Column('income_details', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('expense_details', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('category_wise_analysis', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('pdf_path', sa.String(length=500), nullable=True),
        sa.Column('excel_path', sa.String(length=500), nullable=True),
        sa.Column('generated_by', sa.Integer(), nullable=True),
        sa.Column('generated_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quarterly_reports_report_number'), 'quarterly_reports', ['report_number'], unique=True)
    op.create_index(op.f('ix_quarterly_reports_fy'), 'quarterly_reports', ['financial_year'], unique=False)
    
    # Create report_templates table
    op.create_table(
        'report_templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('template_name', sa.String(length=200), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('report_type', sa.String(length=50), nullable=False),
        sa.Column('fields', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('filters', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('grouping', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('sorting', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('chart_types', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('layout_config', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create dashboard_metrics table
    op.create_table(
        'dashboard_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('metric_date', sa.Date(), nullable=False),
        sa.Column('metric_month', sa.Integer(), nullable=False),
        sa.Column('metric_year', sa.Integer(), nullable=False),
        sa.Column('daily_revenue', sa.Float(), default=0.0),
        sa.Column('monthly_revenue', sa.Float(), default=0.0),
        sa.Column('daily_expenses', sa.Float(), default=0.0),
        sa.Column('monthly_expenses', sa.Float(), default=0.0),
        sa.Column('daily_profit', sa.Float(), default=0.0),
        sa.Column('monthly_profit', sa.Float(), default=0.0),
        sa.Column('total_students', sa.Integer(), default=0),
        sa.Column('new_admissions_today', sa.Integer(), default=0),
        sa.Column('new_admissions_month', sa.Integer(), default=0),
        sa.Column('attendance_percentage', sa.Float(), default=0.0),
        sa.Column('fees_collected_today', sa.Float(), default=0.0),
        sa.Column('fees_collected_month', sa.Float(), default=0.0),
        sa.Column('fees_pending', sa.Float(), default=0.0),
        sa.Column('fee_collection_rate', sa.Float(), default=0.0),
        sa.Column('books_issued_today', sa.Integer(), default=0),
        sa.Column('books_returned_today', sa.Integer(), default=0),
        sa.Column('overdue_books_count', sa.Integer(), default=0),
        sa.Column('fines_collected_today', sa.Float(), default=0.0),
        sa.Column('lost_books_count', sa.Integer(), default=0),
        sa.Column('total_employees', sa.Integer(), default=0),
        sa.Column('employees_on_leave', sa.Integer(), default=0),
        sa.Column('pending_leave_requests', sa.Integer(), default=0),
        sa.Column('upcoming_exams_count', sa.Integer(), default=0),
        sa.Column('pending_results_count', sa.Integer(), default=0),
        sa.Column('revenue_breakdown', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('expense_breakdown', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('student_breakdown', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('last_calculated_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dashboard_metrics_date'), 'dashboard_metrics', ['metric_date'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_dashboard_metrics_date'), table_name='dashboard_metrics')
    op.drop_table('dashboard_metrics')
    op.drop_table('report_templates')
    op.drop_index(op.f('ix_quarterly_reports_fy'), table_name='quarterly_reports')
    op.drop_index(op.f('ix_quarterly_reports_report_number'), table_name='quarterly_reports')
    op.drop_table('quarterly_reports')
    op.drop_index(op.f('ix_incomes_income_number'), table_name='incomes')
    op.drop_table('incomes')
    op.drop_index(op.f('ix_expenses_expense_number'), table_name='expenses')
    op.drop_table('expenses')
    op.drop_index(op.f('ix_journal_entries_account_code'), table_name='journal_entries')
    op.drop_index(op.f('ix_journal_entries_entry_number'), table_name='journal_entries')
    op.drop_table('journal_entries')
    op.drop_index(op.f('ix_income_categories_code'), table_name='income_categories')
    op.drop_table('income_categories')
    op.drop_index(op.f('ix_expense_categories_code'), table_name='expense_categories')
    op.drop_table('expense_categories')
    op.drop_table('emergency_expenses')
    op.drop_table('maintenance_fees')
    op.drop_table('bill_items')
    op.drop_index(op.f('ix_bills_bill_number'), table_name='bills')
    op.drop_index(op.f('ix_bills_id'), table_name='bills')
    op.drop_table('bills')
    op.drop_index(op.f('ix_book_losses_id'), table_name='book_losses')
    op.drop_table('book_losses')
    op.drop_table('lost_book_settings')
