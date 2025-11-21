"""
LMS Views - Learning Management System
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg, Prefetch
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db import transaction
from django.views.decorators.http import require_POST
import csv
from datetime import datetime

from .models import (
    Course, Module, Lesson, Enrollment, LessonProgress,
    Quiz, QuizAttempt, Question, QuizAnswer, Assignment, AssignmentSubmission,
    Discussion, DiscussionReply, Certificate
)
from .forms import (
    CourseForm, ModuleForm, LessonForm, QuizForm,
    AssignmentForm, AssignmentSubmissionForm,
    DiscussionForm, DiscussionReplyForm, EnrollmentForm
)
from .utils import calculate_progress, generate_certificate_number, validate_enrollment


# Dashboard
@login_required
def dashboard(request):
    """LMS dashboard"""
    is_student = hasattr(request.user, 'student_profile')
    is_faculty = hasattr(request.user, 'faculty_profile')
    
    context = {
        'total_courses': Course.objects.published().count(),
        'my_enrollments': 0,
        'active_courses': 0,
        'completed_courses': 0,
        'certificates': 0,
        'is_student': is_student,
        'is_faculty': is_faculty,
    }
    
    if is_student:
        student = request.user.student_profile
        enrollments = Enrollment.objects.filter(student=student)
        context.update({
            'my_enrollments': enrollments.count(),
            'active_courses': enrollments.filter(status='active').count(),
            'completed_courses': enrollments.filter(status='completed').count(),
            'certificates': enrollments.filter(certificate_issued=True).count(),
            'recent_enrollments': enrollments.select_related('course')[:5],
        })
    
    if is_faculty:
        faculty = request.user.faculty_profile
        context.update({
            'teaching_courses': Course.objects.filter(instructor=faculty).count(),
            'total_students': Enrollment.objects.filter(course__instructor=faculty).count(),
        })
    
    return render(request, 'lms/dashboard.html', context)


# Course Views
@login_required
def course_list(request):
    """List all courses"""
    courses = Course.objects.published().select_related('instructor').order_by('-created_at')
    
    # Search
    search = request.GET.get('search')
    if search:
        courses = courses.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) |
            Q(category__icontains=search)
        )
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        courses = courses.filter(category=category)
    
    # Filter by difficulty
    difficulty = request.GET.get('difficulty')
    if difficulty:
        courses = courses.filter(difficulty_level=difficulty)
    
    # Filter by price
    price_filter = request.GET.get('price')
    if price_filter == 'free':
        courses = courses.filter(is_free=True)
    elif price_filter == 'paid':
        courses = courses.filter(is_free=False)
    
    # Get categories for filter
    categories = Course.objects.published().values_list('category', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(courses, 12)
    page = request.GET.get('page')
    courses = paginator.get_page(page)
    
    context = {
        'courses': courses,
        'categories': categories,
        'search': search or '',
    }
    return render(request, 'lms/course_list.html', context)


@login_required
def course_detail(request, pk):
    """Course details"""
    course = get_object_or_404(Course.objects.select_related('instructor'), pk=pk)
    modules = course.modules.filter(is_published=True).prefetch_related(
        Prefetch('lessons', queryset=Lesson.objects.filter(is_published=True))
    ).order_by('order')
    
    is_enrolled = False
    enrollment = None
    progress = 0
    
    if hasattr(request.user, 'student_profile'):
        enrollment = Enrollment.objects.filter(
            student=request.user.student_profile,
            course=course
        ).first()
        is_enrolled = enrollment is not None
        if enrollment:
            progress = float(enrollment.progress_percentage)
    
    # Calculate total duration
    total_duration = sum(module.duration_minutes for module in modules)
    
    # Get discussions
    discussions = course.discussions.select_related('created_by').order_by('-created_at')[:5]
    
    context = {
        'course': course,
        'modules': modules,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'progress': progress,
        'total_duration': total_duration,
        'discussions': discussions,
        'total_lessons': sum(module.lessons.count() for module in modules),
    }
    return render(request, 'lms/course_detail.html', context)


@login_required  
def course_enroll(request, pk):
    """Enroll in a course"""
    course = get_object_or_404(Course, pk=pk)
    
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Only students can enroll in courses')
        return redirect('lms:course_detail', pk=pk)
    
    student = request.user.student_profile
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=student, course=course).exists():
        messages.warning(request, 'Already enrolled in this course')
        return redirect('lms:course_detail', pk=pk)
    
    # Create enrollment
    enrollment = Enrollment.objects.create(
        student=student,
        course=course,
        paid_amount=course.price if not course.is_free else 0,
        payment_status='paid' if course.is_free else 'pending'
    )
    
    # Update enrollment count
    course.enrollment_count += 1
    course.save()
    
    messages.success(request, f'Successfully enrolled in {course.title}')
    return redirect('lms:my_learning')


@login_required
def my_learning(request):
    """Student's enrolled courses"""
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Only students can view learning dashboard')
        return redirect('lms:dashboard')
    
    student = request.user.student_profile
    
    # Get status filter
    status_filter = request.GET.get('status', 'active')
    
    enrollments = Enrollment.objects.filter(student=student)
    
    if status_filter and status_filter != 'all':
        enrollments = enrollments.filter(status=status_filter)
    
    enrollments = enrollments.select_related('course', 'course__instructor').order_by('-enrollment_date')
    
    # Pagination
    paginator = Paginator(enrollments, 10)
    page = request.GET.get('page')
    enrollments = paginator.get_page(page)
    
    # Statistics
    all_enrollments = Enrollment.objects.filter(student=student)
    stats = {
        'total': all_enrollments.count(),
        'active': all_enrollments.filter(status='active').count(),
        'completed': all_enrollments.filter(status='completed').count(),
        'certificates': all_enrollments.filter(certificate_issued=True).count(),
    }
    
    context = {
        'enrollments': enrollments,
        'status_filter': status_filter,
        'stats': stats,
    }
    return render(request, 'lms/my_learning.html', context)


# Lesson Views
@login_required
def lesson_view(request, pk):
    """View lesson content"""
    lesson = get_object_or_404(Lesson.objects.select_related('module__course'), pk=pk)
    course = lesson.module.course
    
    # Check enrollment
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied')
        return redirect('lms:course_detail', pk=course.pk)
    
    enrollment = Enrollment.objects.filter(
        student=request.user.student_profile,
        course=course
    ).first()
    
    if not enrollment and not lesson.is_preview:
        messages.error(request, 'Please enroll in the course to access this lesson')
        return redirect('lms:course_detail', pk=course.pk)
    
    # Track progress
    progress = None
    if enrollment:
        progress, created = LessonProgress.objects.get_or_create(
            enrollment=enrollment,
            lesson=lesson
        )
        progress.last_accessed = timezone.now()
        progress.save()
    
    # Get quizzes and assignments
    quizzes = lesson.quizzes.all()
    assignments = lesson.assignments.all()
    
    # Get navigation (previous and next lessons)
    all_lessons = Lesson.objects.filter(
        module__course=course,
        is_published=True
    ).order_by('module__order', 'order')
    
    lesson_list = list(all_lessons)
    try:
        current_index = lesson_list.index(lesson)
        prev_lesson = lesson_list[current_index - 1] if current_index > 0 else None
        next_lesson = lesson_list[current_index + 1] if current_index < len(lesson_list) - 1 else None
    except ValueError:
        prev_lesson = next_lesson = None
    
    context = {
        'lesson': lesson,
        'course': course,
        'enrollment': enrollment,
        'progress': progress,
        'quizzes': quizzes,
        'assignments': assignments,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
    }
    return render(request, 'lms/lesson_view.html', context)


@login_required
def lesson_complete(request, pk):
    """Mark lesson as complete"""
    lesson = get_object_or_404(Lesson, pk=pk)
    
    if not hasattr(request.user, 'student_profile'):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    enrollment = Enrollment.objects.filter(
        student=request.user.student_profile,
        course=lesson.module.course
    ).first()
    
    if not enrollment:
        return JsonResponse({'error': 'Not enrolled'}, status=403)
    
    progress, created = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )
    
    progress.is_completed = True
    progress.completion_date = timezone.now()
    progress.save()
    
    # Update enrollment progress
    from .utils import calculate_progress
    enrollment.progress_percentage = calculate_progress(enrollment)
    enrollment.save()
    
    return JsonResponse({'success': True, 'progress': float(enrollment.progress_percentage)})


# Placeholder views to prevent URL errors
@login_required
def item_list(request):
    """Redirect to course list"""
    return redirect('lms:course_list')


@login_required
def item_detail(request, pk):
    """Redirect to course detail"""
    return redirect('lms:course_detail', pk=pk)


@login_required
def item_create(request):
    """Create course"""
    if not request.user.is_staff:
        messages.error(request, 'Permission denied')
        return redirect('lms:dashboard')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
            messages.success(request, f'Course "{course.title}" created successfully')
            return redirect('lms:course_detail', pk=course.pk)
    else:
        form = CourseForm()
    
    return render(request, 'lms/course_form.html', {'form': form, 'action': 'Create'})


@login_required
def item_update(request, pk):
    """Update course"""
    course = get_object_or_404(Course, pk=pk)
    
    if not request.user.is_staff:
        messages.error(request, 'Permission denied')
        return redirect('lms:course_detail', pk=pk)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Course "{course.title}" updated successfully')
            return redirect('lms:course_detail', pk=pk)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'lms/course_form.html', {'form': form, 'course': course, 'action': 'Update'})


@login_required
def item_delete(request, pk):
    """Delete course"""
    course = get_object_or_404(Course, pk=pk)
    
    if not request.user.is_staff:
        messages.error(request, 'Permission denied')
        return redirect('lms:course_detail', pk=pk)
    
    if request.method == 'POST':
        title = course.title
        course.delete()
        messages.success(request, f'Course "{title}" deleted successfully')
        return redirect('lms:course_list')
    
    return render(request, 'lms/course_confirm_delete.html', {'course': course})


@login_required
@require_POST
def bulk_delete(request):
    """Bulk delete courses"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    course_ids = request.POST.getlist('course_ids[]')
    if course_ids:
        Course.objects.filter(id__in=course_ids).delete()
        return JsonResponse({'success': True, 'message': f'{len(course_ids)} course(s) deleted'})
    
    return JsonResponse({'error': 'No courses selected'}, status=400)


@login_required
@require_POST
def bulk_update_status(request):
    """Bulk update course status"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    course_ids = request.POST.getlist('course_ids[]')
    new_status = request.POST.get('status')
    
    if course_ids and new_status:
        Course.objects.filter(id__in=course_ids).update(status=new_status)
        return JsonResponse({'success': True, 'message': f'{len(course_ids)} course(s) updated'})
    
    return JsonResponse({'error': 'Invalid data'}, status=400)


@login_required
def export_csv(request):
    """Export courses to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="lms_courses_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Code', 'Title', 'Category', 'Instructor', 'Difficulty', 'Price', 'Status', 'Enrollments'])
    
    courses = Course.objects.select_related('instructor').all()
    for course in courses:
        writer.writerow([
            course.code,
            course.title,
            course.category,
            course.instructor.get_full_name() if course.instructor else '',
            course.difficulty_level,
            course.price,
            course.status,
            course.enrollment_count,
        ])
    
    return response


@login_required
def export_pdf(request):
    """Export courses to PDF"""
    messages.info(request, 'PDF export feature coming soon')
    return redirect('lms:dashboard')


@login_required
def get_item_data(request, pk):
    """Get course data as JSON"""
    course = get_object_or_404(Course, pk=pk)
    
    data = {
        'id': course.id,
        'code': course.code,
        'title': course.title,
        'description': course.description,
        'category': course.category,
        'difficulty_level': course.difficulty_level,
        'price': str(course.price),
        'status': course.status,
        'enrollment_count': course.enrollment_count,
    }
    
    return JsonResponse(data)


@login_required
@require_POST
def toggle_status(request, pk):
    """Toggle course status"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    course = get_object_or_404(Course, pk=pk)
    
    if course.status == 'published':
        course.status = 'draft'
    else:
        course.status = 'published'
        if not course.publish_date:
            course.publish_date = timezone.now()
    
    course.save()
    
    return JsonResponse({'success': True, 'status': course.status})


@login_required
def statistics(request):
    """LMS Statistics"""
    if not request.user.is_staff:
        messages.error(request, 'Permission denied')
        return redirect('lms:dashboard')
    
    stats = {
        'total_courses': Course.objects.count(),
        'published_courses': Course.objects.filter(status='published').count(),
        'draft_courses': Course.objects.filter(status='draft').count(),
        'total_enrollments': Enrollment.objects.count(),
        'active_enrollments': Enrollment.objects.filter(status='active').count(),
        'completed_enrollments': Enrollment.objects.filter(status='completed').count(),
        'certificates_issued': Certificate.objects.count(),
        'total_lessons': Lesson.objects.count(),
        'total_quizzes': Quiz.objects.count(),
        'total_assignments': Assignment.objects.count(),
    }
    
    # Top courses by enrollment
    top_courses = Course.objects.order_by('-enrollment_count')[:10]
    
    # Recent enrollments
    recent_enrollments = Enrollment.objects.select_related('student__user', 'course').order_by('-enrollment_date')[:10]
    
    context = {
        'stats': stats,
        'top_courses': top_courses,
        'recent_enrollments': recent_enrollments,
    }
    
    return render(request, 'lms/statistics.html', context)


@login_required
def search(request):
    """Search courses"""
    query = request.GET.get('q', '')
    if query:
        return redirect(f'/lms/courses/?search={query}')
    return redirect('lms:course_list')


# Quiz Views
@login_required
def quiz_detail(request, pk):
    """Quiz detail and attempt"""
    quiz = get_object_or_404(Quiz.objects.select_related('lesson__module__course'), pk=pk)
    course = quiz.lesson.module.course
    
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied')
        return redirect('lms:course_detail', pk=course.pk)
    
    enrollment = Enrollment.objects.filter(
        student=request.user.student_profile,
        course=course
    ).first()
    
    if not enrollment:
        messages.error(request, 'You must be enrolled in this course')
        return redirect('lms:course_detail', pk=course.pk)
    
    # Get previous attempts
    attempts = QuizAttempt.objects.filter(
        quiz=quiz,
        enrollment=enrollment
    ).order_by('-started_at')
    
    can_attempt = attempts.count() < quiz.max_attempts
    
    context = {
        'quiz': quiz,
        'course': course,
        'enrollment': enrollment,
        'attempts': attempts,
        'can_attempt': can_attempt,
    }
    return render(request, 'lms/quiz_detail.html', context)


@login_required
@require_POST
def quiz_start(request, pk):
    """Start quiz attempt"""
    quiz = get_object_or_404(Quiz, pk=pk)
    
    if not hasattr(request.user, 'student_profile'):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    enrollment = Enrollment.objects.filter(
        student=request.user.student_profile,
        course=quiz.lesson.module.course
    ).first()
    
    if not enrollment:
        return JsonResponse({'error': 'Not enrolled'}, status=403)
    
    # Check attempt limit
    attempt_count = QuizAttempt.objects.filter(quiz=quiz, enrollment=enrollment).count()
    if attempt_count >= quiz.max_attempts:
        return JsonResponse({'error': 'Maximum attempts reached'}, status=400)
    
    # Create attempt
    attempt = QuizAttempt.objects.create(
        quiz=quiz,
        enrollment=enrollment,
        attempt_number=attempt_count + 1
    )
    
    return JsonResponse({'success': True, 'attempt_id': attempt.id})


@login_required
def quiz_take(request, attempt_id):
    """Take quiz"""
    attempt = get_object_or_404(QuizAttempt.objects.select_related('quiz', 'enrollment'), pk=attempt_id)
    
    if not hasattr(request.user, 'student_profile') or attempt.enrollment.student != request.user.student_profile:
        messages.error(request, 'Access denied')
        return redirect('lms:dashboard')
    
    if attempt.status != 'in_progress':
        messages.warning(request, 'This quiz has already been submitted')
        return redirect('lms:quiz_result', attempt_id=attempt_id)
    
    questions = attempt.quiz.questions.all().order_by('order')
    
    if request.method == 'POST':
        # Save answers and grade
        total_points = 0
        earned_points = 0
        
        for question in questions:
            answer_text = request.POST.get(f'question_{question.id}')
            if answer_text:
                is_correct = False
                points = 0
                
                if question.question_type == 'multiple_choice':
                    is_correct = answer_text == question.correct_answer
                    points = float(question.points) if is_correct else 0
                elif question.question_type == 'true_false':
                    is_correct = answer_text.lower() == question.correct_answer.lower()
                    points = float(question.points) if is_correct else 0
                
                QuizAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    answer_text=answer_text,
                    is_correct=is_correct,
                    points_earned=points
                )
                
                earned_points += points
            
            total_points += float(question.points)
        
        # Update attempt
        attempt.score = earned_points
        attempt.total_points = total_points
        attempt.submitted_at = timezone.now()
        attempt.status = 'graded'
        
        if total_points > 0:
            percentage = (earned_points / total_points) * 100
            attempt.passed = percentage >= float(attempt.quiz.passing_score)
        
        attempt.save()
        
        messages.success(request, 'Quiz submitted successfully')
        return redirect('lms:quiz_result', attempt_id=attempt.id)
    
    context = {
        'attempt': attempt,
        'questions': questions,
    }
    return render(request, 'lms/quiz_take.html', context)


@login_required
def quiz_result(request, attempt_id):
    """View quiz results"""
    attempt = get_object_or_404(
        QuizAttempt.objects.select_related('quiz', 'enrollment').prefetch_related('answers__question'),
        pk=attempt_id
    )
    
    if not hasattr(request.user, 'student_profile') or attempt.enrollment.student != request.user.student_profile:
        messages.error(request, 'Access denied')
        return redirect('lms:dashboard')
    
    context = {
        'attempt': attempt,
    }
    return render(request, 'lms/quiz_result.html', context)


# Assignment Views
@login_required
def assignment_detail(request, pk):
    """Assignment detail"""
    assignment = get_object_or_404(Assignment.objects.select_related('lesson__module__course'), pk=pk)
    course = assignment.lesson.module.course
    
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied')
        return redirect('lms:course_detail', pk=course.pk)
    
    enrollment = Enrollment.objects.filter(
        student=request.user.student_profile,
        course=course
    ).first()
    
    if not enrollment:
        messages.error(request, 'You must be enrolled in this course')
        return redirect('lms:course_detail', pk=course.pk)
    
    # Get submission
    submission = AssignmentSubmission.objects.filter(
        assignment=assignment,
        enrollment=enrollment
    ).first()
    
    context = {
        'assignment': assignment,
        'course': course,
        'enrollment': enrollment,
        'submission': submission,
    }
    return render(request, 'lms/assignment_detail.html', context)


@login_required
def assignment_submit(request, pk):
    """Submit assignment"""
    assignment = get_object_or_404(Assignment, pk=pk)
    
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied')
        return redirect('lms:dashboard')
    
    enrollment = Enrollment.objects.filter(
        student=request.user.student_profile,
        course=assignment.lesson.module.course
    ).first()
    
    if not enrollment:
        messages.error(request, 'You must be enrolled in this course')
        return redirect('lms:dashboard')
    
    # Get or create submission
    submission, created = AssignmentSubmission.objects.get_or_create(
        assignment=assignment,
        enrollment=enrollment
    )
    
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            
            # Check if late
            if assignment.due_date and timezone.now() > assignment.due_date:
                submission.is_late = True
            
            submission.status = 'submitted'
            submission.submission_date = timezone.now()
            submission.save()
            
            messages.success(request, 'Assignment submitted successfully')
            return redirect('lms:assignment_detail', pk=assignment.pk)
    else:
        form = AssignmentSubmissionForm(instance=submission)
    
    context = {
        'form': form,
        'assignment': assignment,
        'submission': submission,
    }
    return render(request, 'lms/assignment_submit.html', context)


# Discussion Views
@login_required
def discussion_list(request, course_id):
    """List discussions for a course"""
    course = get_object_or_404(Course, pk=course_id)
    discussions = course.discussions.select_related('created_by').annotate(
        reply_count=Count('replies')
    ).order_by('-is_pinned', '-created_at')
    
    # Pagination
    paginator = Paginator(discussions, 20)
    page = request.GET.get('page')
    discussions = paginator.get_page(page)
    
    context = {
        'course': course,
        'discussions': discussions,
    }
    return render(request, 'lms/discussion_list.html', context)


@login_required
def discussion_detail(request, pk):
    """Discussion detail with replies"""
    discussion = get_object_or_404(
        Discussion.objects.select_related('course', 'created_by'),
        pk=pk
    )
    
    # Increment view count
    discussion.views_count += 1
    discussion.save(update_fields=['views_count'])
    
    replies = discussion.replies.select_related('created_by').order_by('created_at')
    
    if request.method == 'POST':
        form = DiscussionReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.discussion = discussion
            reply.created_by = request.user
            reply.save()
            messages.success(request, 'Reply posted successfully')
            return redirect('lms:discussion_detail', pk=pk)
    else:
        form = DiscussionReplyForm()
    
    context = {
        'discussion': discussion,
        'replies': replies,
        'form': form,
    }
    return render(request, 'lms/discussion_detail.html', context)


@login_required
def discussion_create(request, course_id):
    """Create new discussion"""
    course = get_object_or_404(Course, pk=course_id)
    
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.course = course
            discussion.created_by = request.user
            discussion.save()
            messages.success(request, 'Discussion created successfully')
            return redirect('lms:discussion_detail', pk=discussion.pk)
    else:
        form = DiscussionForm(initial={'course': course})
    
    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'lms/discussion_form.html', context)


# Certificate Views
@login_required
def my_certificates(request):
    """View student's certificates"""
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied')
        return redirect('lms:dashboard')
    
    certificates = Certificate.objects.filter(
        enrollment__student=request.user.student_profile
    ).select_related('enrollment__course').order_by('-issue_date')
    
    context = {
        'certificates': certificates,
    }
    return render(request, 'lms/my_certificates.html', context)


@login_required
def certificate_view(request, pk):
    """View certificate"""
    certificate = get_object_or_404(Certificate.objects.select_related('enrollment__course', 'enrollment__student__user'), pk=pk)
    
    context = {
        'certificate': certificate,
    }
    return render(request, 'lms/certificate_view.html', context)
