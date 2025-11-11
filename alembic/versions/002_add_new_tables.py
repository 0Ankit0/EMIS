"""Add class schedules, exams, marks, result sheets, and library settings tables

Revision ID: 002_add_new_tables
Revises: 001_create_all_tables
Create Date: 2025-11-09 19:01:45

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_add_new_tables'
down_revision = '001_create_all_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create class_schedules table
    op.create_table(
        'class_schedules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('instructor_id', sa.Integer(), nullable=True),
        sa.Column('room_number', sa.String(length=50), nullable=True),
        sa.Column('building', sa.String(length=100), nullable=True),
        sa.Column('day_of_week', sa.Enum('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', name='dayofweek'), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('effective_from', sa.Date(), nullable=False),
        sa.Column('effective_to', sa.Date(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('notes', sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['instructor_id'], ['employees.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_class_schedules_id'), 'class_schedules', ['id'], unique=False)
    
    # Create exams table
    op.create_table(
        'exams',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('exam_name', sa.String(length=200), nullable=False),
        sa.Column('exam_type', sa.Enum('internal', 'external', 'midterm', 'final', 'assignment', 'quiz', 'practical', 'viva', name='examtype'), nullable=False),
        sa.Column('exam_code', sa.String(length=50), nullable=False, unique=True),
        sa.Column('exam_date', sa.Date(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.Column('max_marks', sa.Float(), nullable=False),
        sa.Column('passing_marks', sa.Float(), nullable=False),
        sa.Column('weightage_percentage', sa.Float(), default=100.0),
        sa.Column('venue', sa.String(length=200), nullable=True),
        sa.Column('room_number', sa.String(length=50), nullable=True),
        sa.Column('instructions', sa.Text(), nullable=True),
        sa.Column('syllabus_topics', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('scheduled', 'ongoing', 'completed', 'cancelled', 'postponed', name='examstatus'), nullable=False, default='scheduled'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exams_id'), 'exams', ['id'], unique=False)
    op.create_index(op.f('ix_exams_exam_code'), 'exams', ['exam_code'], unique=True)
    
    # Create marks table
    op.create_table(
        'marks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('exam_id', sa.Integer(), nullable=False),
        sa.Column('enrollment_id', sa.Integer(), nullable=False),
        sa.Column('marks_obtained', sa.Float(), nullable=True),
        sa.Column('max_marks', sa.Float(), nullable=False),
        sa.Column('grade', sa.Enum('A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F', 'P', 'I', 'W', name='gradetype'), nullable=True),
        sa.Column('grade_points', sa.Float(), nullable=True),
        sa.Column('status', sa.Enum('pending', 'submitted', 'verified', 'published', 'withheld', 'absent', name='marksstatus'), nullable=False, default='pending'),
        sa.Column('is_absent', sa.Boolean(), nullable=False, default=False),
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('evaluator_comments', sa.Text(), nullable=True),
        sa.Column('evaluated_by', sa.Integer(), nullable=True),
        sa.Column('evaluated_at', sa.DateTime(), nullable=True),
        sa.Column('verified_by', sa.Integer(), nullable=True),
        sa.Column('verified_at', sa.DateTime(), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['enrollment_id'], ['enrollments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['evaluated_by'], ['employees.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['verified_by'], ['employees.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_marks_id'), 'marks', ['id'], unique=False)
    
    # Create result_sheets table
    op.create_table(
        'result_sheets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('enrollment_id', sa.Integer(), nullable=False),
        sa.Column('result_type', sa.Enum('semester', 'annual', 'cumulative', 'transcript', 'provisional', 'final', name='resulttype'), nullable=False),
        sa.Column('academic_year', sa.String(length=20), nullable=False),
        sa.Column('semester', sa.Integer(), nullable=True),
        sa.Column('total_marks_obtained', sa.Float(), nullable=False, default=0.0),
        sa.Column('total_max_marks', sa.Float(), nullable=False, default=0.0),
        sa.Column('percentage', sa.Float(), nullable=True),
        sa.Column('cgpa', sa.Float(), nullable=True),
        sa.Column('sgpa', sa.Float(), nullable=True),
        sa.Column('grade', sa.String(length=10), nullable=True),
        sa.Column('division', sa.String(length=50), nullable=True),
        sa.Column('rank', sa.Integer(), nullable=True),
        sa.Column('total_students', sa.Integer(), nullable=True),
        sa.Column('is_passed', sa.Boolean(), nullable=False, default=False),
        sa.Column('has_backlogs', sa.Boolean(), nullable=False, default=False),
        sa.Column('backlog_count', sa.Integer(), nullable=False, default=0),
        sa.Column('status', sa.Enum('draft', 'generated', 'verified', 'published', 'withheld', 'cancelled', name='resultstatus'), nullable=False, default='draft'),
        sa.Column('marks_breakdown', sa.JSON(), nullable=True),
        sa.Column('subject_wise_details', sa.JSON(), nullable=True),
        sa.Column('internal_marks_total', sa.Float(), default=0.0),
        sa.Column('external_marks_total', sa.Float(), default=0.0),
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('generated_by', sa.Integer(), nullable=True),
        sa.Column('generated_at', sa.DateTime(), nullable=True),
        sa.Column('verified_by', sa.Integer(), nullable=True),
        sa.Column('verified_at', sa.DateTime(), nullable=True),
        sa.Column('published_by', sa.Integer(), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('result_file_path', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['enrollment_id'], ['enrollments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['generated_by'], ['employees.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['verified_by'], ['employees.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['published_by'], ['employees.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_result_sheets_id'), 'result_sheets', ['id'], unique=False)
    
    # Create library_settings table
    op.create_table(
        'library_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('member_type', sa.Enum('student', 'faculty', 'staff', 'alumni', 'guest', name='membertype'), nullable=False, unique=True),
        sa.Column('max_books_allowed', sa.Integer(), nullable=False, default=3),
        sa.Column('borrowing_period_days', sa.Integer(), nullable=False, default=14),
        sa.Column('fine_per_day', sa.Float(), nullable=False, default=5.0),
        sa.Column('grace_period_days', sa.Integer(), nullable=False, default=0),
        sa.Column('max_fine_amount', sa.Float(), nullable=False, default=500.0),
        sa.Column('max_reservations', sa.Integer(), nullable=False, default=2),
        sa.Column('reservation_hold_days', sa.Integer(), nullable=False, default=3),
        sa.Column('max_renewals', sa.Integer(), nullable=False, default=2),
        sa.Column('digital_access_enabled', sa.Boolean(), nullable=False, default=True),
        sa.Column('digital_download_limit', sa.Integer(), nullable=False, default=10),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('updated_by', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_library_settings_id'), 'library_settings', ['id'], unique=False)
    op.create_index(op.f('ix_library_settings_member_type'), 'library_settings', ['member_type'], unique=True)
    
    # Create fine_waivers table
    op.create_table(
        'fine_waivers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('fine_id', sa.Integer(), nullable=False),
        sa.Column('member_id', sa.Integer(), nullable=False),
        sa.Column('original_amount', sa.Float(), nullable=False),
        sa.Column('waived_amount', sa.Float(), nullable=False),
        sa.Column('final_amount', sa.Float(), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('approved_by', sa.Integer(), nullable=False),
        sa.Column('approved_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fine_waivers_id'), 'fine_waivers', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_fine_waivers_id'), table_name='fine_waivers')
    op.drop_table('fine_waivers')
    
    op.drop_index(op.f('ix_library_settings_member_type'), table_name='library_settings')
    op.drop_index(op.f('ix_library_settings_id'), table_name='library_settings')
    op.drop_table('library_settings')
    
    op.drop_index(op.f('ix_result_sheets_id'), table_name='result_sheets')
    op.drop_table('result_sheets')
    
    op.drop_index(op.f('ix_marks_id'), table_name='marks')
    op.drop_table('marks')
    
    op.drop_index(op.f('ix_exams_exam_code'), table_name='exams')
    op.drop_index(op.f('ix_exams_id'), table_name='exams')
    op.drop_table('exams')
    
    op.drop_index(op.f('ix_class_schedules_id'), table_name='class_schedules')
    op.drop_table('class_schedules')
    
    # Drop enums
    sa.Enum(name='dayofweek').drop(op.get_bind())
    sa.Enum(name='examtype').drop(op.get_bind())
    sa.Enum(name='examstatus').drop(op.get_bind())
    sa.Enum(name='gradetype').drop(op.get_bind())
    sa.Enum(name='marksstatus').drop(op.get_bind())
    sa.Enum(name='resulttype').drop(op.get_bind())
    sa.Enum(name='resultstatus').drop(op.get_bind())
    sa.Enum(name='membertype').drop(op.get_bind())
