"""Add billing enhancements for installments, late fees, and email tracking

Revision ID: billing_enhancements_001
Revises: 
Create Date: 2025-11-10

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'billing_enhancements_001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add columns to bills table
    op.add_column('bills', sa.Column('has_installments', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('bills', sa.Column('installments', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('bills', sa.Column('late_fee_applied', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('bills', sa.Column('late_fee_amount', sa.Float(), nullable=False, server_default='0.0'))
    op.add_column('bills', sa.Column('email_sent', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('bills', sa.Column('email_sent_date', sa.DateTime(), nullable=True))
    op.add_column('bills', sa.Column('email_recipient', sa.String(length=255), nullable=True))


def downgrade():
    # Remove columns from bills table
    op.drop_column('bills', 'email_recipient')
    op.drop_column('bills', 'email_sent_date')
    op.drop_column('bills', 'email_sent')
    op.drop_column('bills', 'late_fee_amount')
    op.drop_column('bills', 'late_fee_applied')
    op.drop_column('bills', 'installments')
    op.drop_column('bills', 'has_installments')
