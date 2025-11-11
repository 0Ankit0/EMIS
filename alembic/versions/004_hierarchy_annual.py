"""Add teacher hierarchy and annual reports

Revision ID: 004_hierarchy_annual
Revises: 003_billing_reporting
Create Date: 2025-11-09 15:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004_hierarchy_annual'
down_revision = '003_billing_reporting'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create teacher_hierarchy table
    op.create_table(
        'teacher_hierarchy',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('teacher_id', sa.Integer(), nullable=False),
        sa.Column('designation', sa.String(length=100), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('reports_to', sa.Integer(), nullable=True),
        sa.Column('hierarchy_level', sa.Integer(), nullable=False, default=3),
        sa.Column('is_department_head', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_program_coordinator', sa.Boolean(), nullable=False, default=False),
        sa.Column('program_id', sa.Integer(), nullable=True),
        sa.Column('subject_coordinator_ids', postgresql.ARRAY(sa.Integer()), nullable=True),
        sa.Column('effective_from', sa.Date(), nullable=False),
        sa.Column('effective_to', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['teacher_id'], ['employees.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['reports_to'], ['employees.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teacher_hierarchy_id'), 'teacher_hierarchy', ['id'], unique=False)
    op.create_index(op.f('ix_teacher_hierarchy_teacher'), 'teacher_hierarchy', ['teacher_id'], unique=False)
    
    # Create department_hierarchy table
    op.create_table(
        'department_hierarchy',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('parent_department_id', sa.Integer(), nullable=True),
        sa.Column('hierarchy_level', sa.Integer(), nullable=False, default=1),
        sa.Column('head_of_department_id', sa.Integer(), nullable=True),
        sa.Column('annual_budget', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_department_id'], ['departments.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['head_of_department_id'], ['employees.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_department_hierarchy_dept'), 'department_hierarchy', ['department_id'], unique=True)
    
    # Create annual_financial_reports table
    op.create_table(
        'annual_financial_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('report_number', sa.String(length=50), nullable=False, unique=True),
        sa.Column('report_type', sa.String(length=50), nullable=False),
        sa.Column('financial_year', sa.String(length=20), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        
        # Executive Summary
        sa.Column('total_annual_revenue', sa.Float(), default=0.0),
        sa.Column('total_annual_expenses', sa.Float(), default=0.0),
        sa.Column('net_annual_profit_loss', sa.Float(), default=0.0),
        sa.Column('annual_profit_margin', sa.Float(), default=0.0),
        
        # Quarterly breakdown
        sa.Column('q1_income', sa.Float(), default=0.0),
        sa.Column('q2_income', sa.Float(), default=0.0),
        sa.Column('q3_income', sa.Float(), default=0.0),
        sa.Column('q4_income', sa.Float(), default=0.0),
        sa.Column('q1_expenses', sa.Float(), default=0.0),
        sa.Column('q2_expenses', sa.Float(), default=0.0),
        sa.Column('q3_expenses', sa.Float(), default=0.0),
        sa.Column('q4_expenses', sa.Float(), default=0.0),
        
        # JSON data
        sa.Column('monthly_income_breakdown', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('monthly_expense_breakdown', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('income_by_category', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('expenses_by_category', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        
        # Salary analysis
        sa.Column('total_salary_expenses', sa.Float(), default=0.0),
        sa.Column('faculty_salary_total', sa.Float(), default=0.0),
        sa.Column('staff_salary_total', sa.Float(), default=0.0),
        sa.Column('department_wise_salary', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('designation_wise_salary', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        
        # Department performance
        sa.Column('department_income', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('department_expenses', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('department_profitability', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        
        # Student metrics
        sa.Column('year_start_enrollment', sa.Integer(), default=0),
        sa.Column('year_end_enrollment', sa.Integer(), default=0),
        sa.Column('total_admissions', sa.Integer(), default=0),
        sa.Column('total_graduations', sa.Integer(), default=0),
        sa.Column('program_enrollment', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('annual_fees_collected', sa.Float(), default=0.0),
        sa.Column('annual_fees_outstanding', sa.Float(), default=0.0),
        sa.Column('collection_rate', sa.Float(), default=0.0),
        
        # Faculty metrics
        sa.Column('total_faculty_count', sa.Integer(), default=0),
        sa.Column('department_faculty_count', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('faculty_student_ratio', sa.Float(), default=0.0),
        
        # Balance sheet
        sa.Column('total_assets', sa.Float(), default=0.0),
        sa.Column('current_assets', sa.Float(), default=0.0),
        sa.Column('fixed_assets', sa.Float(), default=0.0),
        sa.Column('total_liabilities', sa.Float(), default=0.0),
        sa.Column('current_liabilities', sa.Float(), default=0.0),
        sa.Column('long_term_liabilities', sa.Float(), default=0.0),
        sa.Column('total_equity', sa.Float(), default=0.0),
        
        # Cash flow
        sa.Column('operating_cash_flow', sa.Float(), default=0.0),
        sa.Column('investing_cash_flow', sa.Float(), default=0.0),
        sa.Column('financing_cash_flow', sa.Float(), default=0.0),
        sa.Column('net_cash_flow', sa.Float(), default=0.0),
        
        # Financial ratios
        sa.Column('current_ratio', sa.Float(), default=0.0),
        sa.Column('quick_ratio', sa.Float(), default=0.0),
        sa.Column('debt_to_equity', sa.Float(), default=0.0),
        sa.Column('return_on_assets', sa.Float(), default=0.0),
        sa.Column('operating_margin', sa.Float(), default=0.0),
        
        # Comparative
        sa.Column('previous_year_comparison', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('year_over_year_growth', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        
        # Trends
        sa.Column('income_trend', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('expense_trend', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('enrollment_trend', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        
        # Metadata
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('pdf_path', sa.String(length=500), nullable=True),
        sa.Column('excel_path', sa.String(length=500), nullable=True),
        sa.Column('generated_by', sa.Integer(), nullable=True),
        sa.Column('approved_by', sa.Integer(), nullable=True),
        sa.Column('generated_at', sa.DateTime(), nullable=True),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_annual_reports_number'), 'annual_financial_reports', ['report_number'], unique=True)
    op.create_index(op.f('ix_annual_reports_fy'), 'annual_financial_reports', ['financial_year'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_annual_reports_fy'), table_name='annual_financial_reports')
    op.drop_index(op.f('ix_annual_reports_number'), table_name='annual_financial_reports')
    op.drop_table('annual_financial_reports')
    
    op.drop_index(op.f('ix_department_hierarchy_dept'), table_name='department_hierarchy')
    op.drop_table('department_hierarchy')
    
    op.drop_index(op.f('ix_teacher_hierarchy_teacher'), table_name='teacher_hierarchy')
    op.drop_index(op.f('ix_teacher_hierarchy_id'), table_name='teacher_hierarchy')
    op.drop_table('teacher_hierarchy')
