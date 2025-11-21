"""
Exams Utility Functions
"""
from django.core.exceptions import ValidationError
from django.utils import timezone
from io import StringIO, BytesIO
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def validate_exam_data(data):
    """
    Validate exam data
    
    Args:
        data: Dictionary of data to validate
    
    Returns:
        bool: True if valid
    
    Raises:
        ValidationError: If validation fails
    """
    if not data.get('exam_code'):
        raise ValidationError("Exam code is required")
    
    if not data.get('exam_name'):
        raise ValidationError("Exam name is required")
    
    if data.get('passing_marks', 0) > data.get('total_marks', 100):
        raise ValidationError("Passing marks cannot be greater than total marks")
    
    return True


def generate_exam_report(queryset):
    """
    Generate report for exams
    
    Args:
        queryset: QuerySet of exams
    
    Returns:
        dict: Report data
    """
    return {
        'total': queryset.count(),
        'scheduled': queryset.filter(status='scheduled').count(),
        'ongoing': queryset.filter(status='ongoing').count(),
        'completed': queryset.filter(status='completed').count(),
        'cancelled': queryset.filter(status='cancelled').count(),
        'by_type': {
            'midterm': queryset.filter(exam_type='midterm').count(),
            'final': queryset.filter(exam_type='final').count(),
            'quiz': queryset.filter(exam_type='quiz').count(),
            'practical': queryset.filter(exam_type='practical').count(),
        }
    }


def export_exams_to_csv(queryset):
    """
    Export exams to CSV
    
    Args:
        queryset: QuerySet of exams to export
    
    Returns:
        str: CSV data
    """
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Exam Code', 'Exam Name', 'Course', 'Academic Year', 'Semester',
        'Exam Date', 'Start Time', 'End Time', 'Duration (mins)',
        'Total Marks', 'Passing Marks', 'Exam Type', 'Room', 'Status'
    ])
    
    # Write data
    for exam in queryset:
        writer.writerow([
            exam.exam_code,
            exam.exam_name,
            exam.course.course_name if exam.course else '',
            exam.academic_year,
            exam.semester,
            exam.exam_date.strftime('%Y-%m-%d'),
            exam.start_time.strftime('%H:%M'),
            exam.end_time.strftime('%H:%M'),
            exam.duration_minutes,
            exam.total_marks,
            exam.passing_marks,
            exam.get_exam_type_display(),
            exam.room_number,
            exam.get_status_display(),
        ])
    
    return output.getvalue()


def export_results_to_csv(queryset):
    """
    Export exam results to CSV
    
    Args:
        queryset: QuerySet of exam results to export
    
    Returns:
        str: CSV data
    """
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Exam Code', 'Exam Name', 'Student Roll Number', 'Student Name',
        'Marks Obtained', 'Total Marks', 'Grade', 'Percentage',
        'Status', 'Absent', 'Remarks'
    ])
    
    # Write data
    for result in queryset:
        writer.writerow([
            result.exam.exam_code,
            result.exam.exam_name,
            result.student.roll_number,
            result.student.get_full_name(),
            result.marks_obtained,
            result.exam.total_marks,
            result.grade,
            f"{result.get_percentage():.2f}%",
            'Passed' if result.is_passed else 'Failed',
            'Yes' if result.is_absent else 'No',
            result.remarks,
        ])
    
    return output.getvalue()


def process_bulk_results_csv(exam, csv_file, user):
    """
    Process bulk result upload CSV
    
    Args:
        exam: Exam instance
        csv_file: CSV file object
        user: User performing the upload
    
    Returns:
        tuple: (success_count, errors)
    """
    from .models import ExamResult
    from apps.students.models import Student
    
    errors = []
    success_count = 0
    
    # Read CSV
    decoded_file = csv_file.read().decode('utf-8')
    csv_reader = csv.DictReader(StringIO(decoded_file))
    
    for row_num, row in enumerate(csv_reader, start=2):
        try:
            # Get student by roll number
            roll_number = row.get('roll_number', '').strip()
            marks = row.get('marks', '').strip()
            is_absent = row.get('absent', '').strip().lower() in ['yes', 'true', '1']
            remarks = row.get('remarks', '').strip()
            
            if not roll_number:
                errors.append(f"Row {row_num}: Roll number is required")
                continue
            
            try:
                student = Student.objects.get(roll_number=roll_number)
            except Student.DoesNotExist:
                errors.append(f"Row {row_num}: Student with roll number {roll_number} not found")
                continue
            
            # Validate marks
            if not is_absent:
                if not marks:
                    errors.append(f"Row {row_num}: Marks required for {roll_number}")
                    continue
                
                try:
                    marks_float = float(marks)
                    if marks_float > exam.total_marks:
                        errors.append(f"Row {row_num}: Marks exceed total marks for {roll_number}")
                        continue
                except ValueError:
                    errors.append(f"Row {row_num}: Invalid marks value for {roll_number}")
                    continue
            else:
                marks_float = 0
            
            # Create or update result
            result, created = ExamResult.objects.update_or_create(
                exam=exam,
                student=student,
                defaults={
                    'marks_obtained': marks_float,
                    'is_absent': is_absent,
                    'remarks': remarks,
                    'evaluated_by': user.faculty if hasattr(user, 'faculty') else None,
                    'evaluated_at': timezone.now()
                }
            )
            success_count += 1
            
        except Exception as e:
            errors.append(f"Row {row_num}: {str(e)}")
    
    return success_count, errors


def generate_result_card_pdf(result):
    """
    Generate PDF result card for a student
    
    Args:
        result: ExamResult instance
    
    Returns:
        bytes: PDF data
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"<b>RESULT CARD</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Student Info
    student_info = [
        ['Student Name:', result.student.get_full_name()],
        ['Roll Number:', result.student.roll_number],
        ['', ''],
    ]
    
    # Exam Info
    exam_info = [
        ['Exam Code:', result.exam.exam_code],
        ['Exam Name:', result.exam.exam_name],
        ['Course:', result.exam.course.course_name],
        ['Exam Date:', result.exam.exam_date.strftime('%B %d, %Y')],
        ['', ''],
    ]
    
    # Result Info
    result_info = [
        ['Marks Obtained:', f"{result.marks_obtained} / {result.exam.total_marks}"],
        ['Percentage:', f"{result.get_percentage():.2f}%"],
        ['Grade:', result.grade],
        ['Status:', 'PASSED' if result.is_passed else 'FAILED' if not result.is_absent else 'ABSENT'],
    ]
    
    # Create tables
    for info in [student_info, exam_info, result_info]:
        table = Table(info, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Remarks
    if result.remarks:
        elements.append(Paragraph(f"<b>Remarks:</b> {result.remarks}", styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    
    return buffer.getvalue()


def calculate_grade_from_percentage(percentage):
    """
    Calculate grade from percentage
    
    Args:
        percentage: Percentage value
    
    Returns:
        str: Grade letter
    """
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B+'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C+'
    elif percentage >= 40:
        return 'C'
    elif percentage >= 33:
        return 'D'
    else:
        return 'F'


def get_exam_statistics(exam):
    """
    Get detailed statistics for an exam
    
    Args:
        exam: Exam instance
    
    Returns:
        dict: Statistics data
    """
    results = exam.results.all()
    
    total = results.count()
    passed = results.filter(is_passed=True).count()
    failed = results.filter(is_passed=False, is_absent=False).count()
    absent = results.filter(is_absent=True).count()
    
    # Grade distribution
    grade_dist = {}
    for grade in ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F']:
        grade_dist[grade] = results.filter(grade=grade).count()
    
    # Calculate averages
    attended = results.filter(is_absent=False)
    avg_marks = attended.aggregate(avg=models.Avg('marks_obtained'))['avg'] or 0
    max_marks = attended.aggregate(max=models.Max('marks_obtained'))['max'] or 0
    min_marks = attended.aggregate(min=models.Min('marks_obtained'))['min'] or 0
    
    return {
        'total_students': total,
        'passed': passed,
        'failed': failed,
        'absent': absent,
        'pass_percentage': (passed / total * 100) if total > 0 else 0,
        'grade_distribution': grade_dist,
        'average_marks': avg_marks,
        'highest_marks': max_marks,
        'lowest_marks': min_marks,
    }
