"""
LMS Utility Functions
"""
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from decimal import Decimal


def calculate_progress(enrollment):
    """
    Calculate course progress for an enrollment
    
    Args:
        enrollment: Enrollment instance
    
    Returns:
        Decimal: Progress percentage
    """
    from .models import LessonProgress, Lesson
    
    total_lessons = Lesson.objects.filter(
        module__course=enrollment.course,
        is_published=True
    ).count()
    
    if total_lessons == 0:
        return Decimal('0.00')
    
    completed_lessons = LessonProgress.objects.filter(
        enrollment=enrollment,
        is_completed=True
    ).count()
    
    progress = (completed_lessons / total_lessons) * 100
    return Decimal(str(round(progress, 2)))


def generate_certificate_number(enrollment):
    """
    Generate unique certificate number
    
    Args:
        enrollment: Enrollment instance
    
    Returns:
        str: Certificate number
    """
    year = timezone.now().year
    course_code = enrollment.course.code
    student_id = enrollment.student.id
    
    return f"CERT-{year}-{course_code}-{student_id:06d}"


def check_quiz_pass(attempt):
    """
    Check if quiz attempt passed
    
    Args:
        attempt: QuizAttempt instance
    
    Returns:
        bool: True if passed
    """
    if attempt.total_points == 0:
        return False
    
    percentage = (attempt.score / attempt.total_points) * 100
    return percentage >= float(attempt.quiz.passing_score)


def calculate_assignment_late_penalty(submission, assignment):
    """
    Calculate late submission penalty
    
    Args:
        submission: AssignmentSubmission instance
        assignment: Assignment instance
    
    Returns:
        Decimal: Penalty amount
    """
    if not submission.is_late or not assignment.allow_late_submission:
        return Decimal('0.00')
    
    penalty_percentage = assignment.late_penalty_percentage
    max_points = assignment.max_points
    
    penalty = (max_points * penalty_percentage) / 100
    return Decimal(str(round(penalty, 2)))


def export_course_to_csv(course):
    """
    Export course structure to CSV
    
    Args:
        course: Course instance
    
    Returns:
        str: CSV data
    """
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Module', 'Lesson', 'Type', 'Duration (min)', 'Published'])
    
    for module in course.modules.all():
        for lesson in module.lessons.all():
            writer.writerow([
                module.title,
                lesson.title,
                lesson.content_type,
                lesson.duration_minutes,
                'Yes' if lesson.is_published else 'No'
            ])
    
    return output.getvalue()


def get_student_course_stats(student):
    """
    Get student's course statistics
    
    Args:
        student: Student instance
    
    Returns:
        dict: Statistics
    """
    from .models import Enrollment
    
    enrollments = Enrollment.objects.filter(student=student)
    
    return {
        'total_enrolled': enrollments.count(),
        'active': enrollments.filter(status='active').count(),
        'completed': enrollments.filter(status='completed').count(),
        'certificates_earned': enrollments.filter(certificate_issued=True).count(),
        'average_progress': enrollments.aggregate(
            avg_progress=models.Avg('progress_percentage')
        )['avg_progress'] or 0,
    }


def validate_enrollment(student, course):
    """
    Validate if student can enroll in course
    
    Args:
        student: Student instance
        course: Course instance
    
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    from .models import Enrollment
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=student, course=course).exists():
        return False, "Already enrolled in this course"
    
    # Check if course is full
    if course.is_full:
        return False, "Course is full"
    
    # Check if course is published
    if course.status != 'published':
        return False, "Course is not available"
    
    return True, ""
