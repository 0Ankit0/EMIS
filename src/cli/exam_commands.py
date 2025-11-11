"""CLI commands for exam and marks management"""
import asyncio
import click
from datetime import datetime, date
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.services.exam_service import ExamService
from src.services.marks_service import MarksService
from src.services.result_service import ResultService
from src.models.exam import ExamType, ExamStatus
from src.models.result_sheet import ResultType


# Create async engine and session
engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@click.group()
def exam():
    """Exam and marks management commands"""
    pass


@exam.command()
@click.option('--course-id', type=int, required=True, help='Course ID')
@click.option('--name', required=True, help='Exam name')
@click.option('--code', required=True, help='Unique exam code')
@click.option('--type', 'exam_type', type=click.Choice(['midterm', 'final', 'quiz', 'assignment']), 
              default='midterm', help='Exam type')
@click.option('--date', 'exam_date', type=click.DateTime(formats=['%Y-%m-%d']), required=True, help='Exam date')
@click.option('--max-marks', type=float, default=100.0, help='Maximum marks')
@click.option('--passing-marks', type=float, default=40.0, help='Passing marks')
def create(course_id, name, code, exam_type, exam_date, max_marks, passing_marks):
    """Create a new exam"""
    async def _create():
        async with AsyncSessionLocal() as session:
            service = ExamService(session)
            
            # Check if code exists
            existing = await service.get_exam_by_code(code)
            if existing:
                click.echo(f"✗ Exam with code '{code}' already exists")
                return
            
            # Create exam
            exam_data = {
                "course_id": course_id,
                "exam_name": name,
                "exam_type": ExamType(exam_type),
                "exam_code": code,
                "exam_date": exam_date.date(),
                "start_time": datetime.combine(exam_date.date(), datetime.min.time()),
                "end_time": datetime.combine(exam_date.date(), datetime.min.time()),
                "duration_minutes": 120,
                "max_marks": max_marks,
                "passing_marks": passing_marks
            }
            
            exam = await service.create_exam(**exam_data, created_by=1)
            
            click.echo(f"✓ Created exam: {exam.exam_name} (ID: {exam.id})")
            click.echo(f"  Code: {exam.exam_code}")
            click.echo(f"  Type: {exam.exam_type.value}")
            click.echo(f"  Date: {exam.exam_date}")
            click.echo(f"  Marks: {exam.max_marks} (Passing: {exam.passing_marks})")
    
    asyncio.run(_create())


@exam.command()
@click.argument('exam_id', type=int)
def show(exam_id):
    """Show exam details"""
    async def _show():
        async with AsyncSessionLocal() as session:
            service = ExamService(session)
            exam = await service.get_exam_by_id(exam_id)
            
            if not exam:
                click.echo(f"✗ Exam with ID {exam_id} not found")
                return
            
            click.echo(f"\nExam Details:")
            click.echo("=" * 60)
            click.echo(f"ID: {exam.id}")
            click.echo(f"Name: {exam.exam_name}")
            click.echo(f"Code: {exam.exam_code}")
            click.echo(f"Type: {exam.exam_type.value}")
            click.echo(f"Course ID: {exam.course_id}")
            click.echo(f"Date: {exam.exam_date}")
            click.echo(f"Status: {exam.status.value}")
            click.echo(f"Max Marks: {exam.max_marks}")
            click.echo(f"Passing Marks: {exam.passing_marks}")
            click.echo(f"Weightage: {exam.weightage_percentage}%")
    
    asyncio.run(_show())


@exam.command()
@click.option('--days', type=int, default=30, help='Days ahead to check')
def upcoming(days):
    """List upcoming exams"""
    async def _upcoming():
        async with AsyncSessionLocal() as session:
            service = ExamService(session)
            exams = await service.get_upcoming_exams(days)
            
            if not exams:
                click.echo(f"✗ No upcoming exams in the next {days} days")
                return
            
            click.echo(f"\nUpcoming Exams (next {days} days):")
            click.echo("=" * 80)
            
            for exam in exams:
                click.echo(f"\n{exam.exam_name}")
                click.echo(f"  Code: {exam.exam_code}")
                click.echo(f"  Date: {exam.exam_date}")
                click.echo(f"  Type: {exam.exam_type.value}")
                click.echo(f"  Max Marks: {exam.max_marks}")
    
    asyncio.run(_upcoming())


@exam.command()
@click.argument('exam_id', type=int)
@click.argument('student_id', type=int)
@click.option('--enrollment-id', type=int, required=True, help='Enrollment ID')
@click.option('--marks', type=float, required=True, help='Marks obtained')
def add_marks(exam_id, student_id, enrollment_id, marks):
    """Add marks for a student in an exam"""
    async def _add():
        async with AsyncSessionLocal() as session:
            exam_service = ExamService(session)
            marks_service = MarksService(session)
            
            # Verify exam exists
            exam = await exam_service.get_exam_by_id(exam_id)
            if not exam:
                click.echo(f"✗ Exam with ID {exam_id} not found")
                return
            
            # Create marks entry
            marks_data = {
                "student_id": student_id,
                "exam_id": exam_id,
                "enrollment_id": enrollment_id,
                "marks_obtained": marks,
                "max_marks": exam.max_marks
            }
            
            result = await marks_service.create_marks(**marks_data, evaluator_id=1)
            
            click.echo(f"✓ Added marks for student {student_id}")
            click.echo(f"  Exam: {exam.exam_name}")
            click.echo(f"  Marks: {result.marks_obtained}/{result.max_marks}")
            click.echo(f"  Grade: {result.grade.value if result.grade else 'N/A'}")
    
    asyncio.run(_add())


@exam.command()
@click.argument('exam_id', type=int)
def publish_all_marks(exam_id):
    """Publish all verified marks for an exam"""
    async def _publish():
        async with AsyncSessionLocal() as session:
            marks_service = MarksService(session)
            
            count = await marks_service.bulk_publish_marks(exam_id, publisher_id=1)
            
            if count > 0:
                click.echo(f"✓ Published marks for {count} students")
            else:
                click.echo(f"✗ No verified marks found to publish for exam {exam_id}")
    
    asyncio.run(_publish())


@exam.command()
@click.option('--student-id', type=int, required=True, help='Student ID')
@click.option('--enrollment-id', type=int, required=True, help='Enrollment ID')
@click.option('--type', 'result_type', type=click.Choice(['semester', 'annual', 'transcript']),
              default='semester', help='Result type')
@click.option('--year', required=True, help='Academic year (e.g., 2023-2024)')
@click.option('--semester', type=int, help='Semester number')
def generate_result(student_id, enrollment_id, result_type, year, semester):
    """Generate result sheet for a student"""
    async def _generate():
        async with AsyncSessionLocal() as session:
            service = ResultService(session)
            
            result = await service.generate_result_sheet(
                student_id=student_id,
                enrollment_id=enrollment_id,
                result_type=ResultType(result_type),
                academic_year=year,
                semester=semester,
                generated_by=1
            )
            
            click.echo(f"✓ Generated result sheet (ID: {result.id})")
            click.echo(f"  Student: {result.student_id}")
            click.echo(f"  Type: {result.result_type.value}")
            click.echo(f"  Year: {result.academic_year}")
            if result.semester:
                click.echo(f"  Semester: {result.semester}")
            click.echo(f"  Marks: {result.total_marks_obtained}/{result.total_max_marks}")
            click.echo(f"  Percentage: {result.percentage:.2f}%")
            click.echo(f"  CGPA: {result.cgpa or 'N/A'}")
            click.echo(f"  Status: {'PASSED' if result.is_passed else 'FAILED'}")
    
    asyncio.run(_generate())


if __name__ == '__main__':
    exam()
