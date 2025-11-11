"""Add academic calendar tables

Revision ID: add_academic_calendar
Revises: 
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_academic_calendar'
down_revision = None  # Set this to previous migration
branch_labels = None
depends_on = None


def upgrade():
    # Create academic_calendar table
    op.create_table(
        'academic_calendar',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('start_date', sa.Date, nullable=False),
        sa.Column('end_date', sa.Date),
        sa.Column('start_time', sa.Time),
        sa.Column('end_time', sa.Time),
        sa.Column('is_all_day', sa.Boolean, default=True),
        sa.Column('academic_year', sa.String(20)),
        sa.Column('semester', sa.Integer),
        sa.Column('program_id', sa.Integer, sa.ForeignKey('programs.id')),
        sa.Column('department_id', sa.Integer),
        sa.Column('location', sa.String(500)),
        sa.Column('venue', sa.String(500)),
        sa.Column('organizer', sa.String(200)),
        sa.Column('contact_person', sa.String(200)),
        sa.Column('contact_email', sa.String(200)),
        sa.Column('contact_phone', sa.String(20)),
        sa.Column('status', sa.String(50), default='scheduled'),
        sa.Column('is_published', sa.Boolean, default=False),
        sa.Column('is_recurring', sa.Boolean, default=False),
        sa.Column('recurrence_rule', sa.Text),
        sa.Column('is_for_students', sa.Boolean, default=True),
        sa.Column('is_for_faculty', sa.Boolean, default=True),
        sa.Column('is_for_staff', sa.Boolean, default=False),
        sa.Column('is_for_parents', sa.Boolean, default=False),
        sa.Column('is_public', sa.Boolean, default=False),
        sa.Column('color_code', sa.String(20)),
        sa.Column('icon', sa.String(50)),
        sa.Column('priority', sa.Integer, default=0),
        sa.Column('registration_url', sa.String(500)),
        sa.Column('resource_links', postgresql.JSONB),
        sa.Column('exam_id', sa.Integer, sa.ForeignKey('exams.id')),
        sa.Column('exam_routine_id', sa.Integer),
        sa.Column('admission_batch_id', sa.Integer),
        sa.Column('send_reminder', sa.Boolean, default=True),
        sa.Column('reminder_days_before', sa.Integer, default=1),
        sa.Column('reminder_sent', sa.Boolean, default=False),
        sa.Column('created_by', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_by', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now()),
        sa.Column('published_by', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('published_at', sa.DateTime),
        sa.Column('cancelled_at', sa.DateTime),
        sa.Column('cancelled_by', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('cancellation_reason', sa.Text),
        sa.Column('postponed_to_date', sa.Date),
        sa.Column('attachments', postgresql.JSONB),
        sa.Column('notes', sa.Text),
    )
    
    # Create holidays table
    op.create_table(
        'holidays',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('holiday_date', sa.Date, nullable=False),
        sa.Column('holiday_type', sa.String(50)),
        sa.Column('is_restricted', sa.Boolean, default=False),
        sa.Column('academic_year', sa.String(20)),
        sa.Column('is_for_students', sa.Boolean, default=True),
        sa.Column('is_for_faculty', sa.Boolean, default=True),
        sa.Column('is_for_staff', sa.Boolean, default=True),
        sa.Column('created_by', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now()),
        sa.Column('calendar_event_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('academic_calendar.id')),
    )
    
    # Create important_dates table
    op.create_table(
        'important_dates',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('deadline_date', sa.Date, nullable=False),
        sa.Column('deadline_time', sa.Time),
        sa.Column('category', sa.String(100)),
        sa.Column('academic_year', sa.String(20)),
        sa.Column('semester', sa.Integer),
        sa.Column('send_notification', sa.Boolean, default=True),
        sa.Column('notification_days', sa.Integer, default=3),
        sa.Column('created_by', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('calendar_event_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('academic_calendar.id')),
    )
    
    # Create calendar_subscriptions table
    op.create_table(
        'calendar_subscriptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('event_types', postgresql.JSONB),
        sa.Column('programs', postgresql.JSONB),
        sa.Column('departments', postgresql.JSONB),
        sa.Column('email_notifications', sa.Boolean, default=True),
        sa.Column('sms_notifications', sa.Boolean, default=False),
        sa.Column('push_notifications', sa.Boolean, default=True),
        sa.Column('ical_token', sa.String(100), unique=True),
        sa.Column('ical_url', sa.String(500)),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now()),
    )
    
    # Create indexes
    op.create_index('idx_calendar_start_date', 'academic_calendar', ['start_date'])
    op.create_index('idx_calendar_event_type', 'academic_calendar', ['event_type'])
    op.create_index('idx_calendar_academic_year', 'academic_calendar', ['academic_year'])
    op.create_index('idx_calendar_is_published', 'academic_calendar', ['is_published'])
    op.create_index('idx_holidays_date', 'holidays', ['holiday_date'])
    op.create_index('idx_deadlines_date', 'important_dates', ['deadline_date'])


def downgrade():
    op.drop_index('idx_deadlines_date')
    op.drop_index('idx_holidays_date')
    op.drop_index('idx_calendar_is_published')
    op.drop_index('idx_calendar_academic_year')
    op.drop_index('idx_calendar_event_type')
    op.drop_index('idx_calendar_start_date')
    
    op.drop_table('calendar_subscriptions')
    op.drop_table('important_dates')
    op.drop_table('holidays')
    op.drop_table('academic_calendar')
