"""
LMS Models - Complete Learning Management System
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel
from decimal import Decimal
from .managers import CourseManager, EnrollmentManager

User = get_user_model()


class Course(TimeStampedModel):
    """Online Course"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=300)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    
    category = models.CharField(max_length=100)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    
    instructor = models.ForeignKey('faculty.Faculty', on_delete=models.SET_NULL, null=True, related_name='lms_courses')
    
    thumbnail = models.ImageField(upload_to='lms/course_thumbnails/', blank=True, null=True)
    intro_video = models.FileField(upload_to='lms/course_videos/', blank=True, null=True)
    
    duration_hours = models.IntegerField(help_text="Estimated course duration in hours")
    
    prerequisites = models.TextField(blank=True)
    learning_objectives = models.TextField(blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    is_free = models.BooleanField(default=False)
    
    max_enrollments = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    enrollment_count = models.IntegerField(default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    
    publish_date = models.DateTimeField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_courses')
    
    objects = CourseManager()
    
    class Meta:
        db_table = 'lms_courses'
        ordering = ['-created_at']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['status', 'publish_date']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.title}"
    
    @property
    def is_full(self):
        if self.max_enrollments:
            return self.enrollment_count >= self.max_enrollments
        return False


class Module(TimeStampedModel):
    """Course Module/Section"""
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    duration_minutes = models.IntegerField(default=0)
    
    is_published = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'lms_modules'
        ordering = ['course', 'order']
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"


class Lesson(TimeStampedModel):
    """Course Lesson/Lecture"""
    
    CONTENT_TYPE_CHOICES = [
        ('video', 'Video'),
        ('text', 'Text/Article'),
        ('pdf', 'PDF Document'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('live', 'Live Session'),
    ]
    
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    
    title = models.CharField(max_length=300)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    order = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=0)
    
    # Content fields
    text_content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to='lms/lesson_videos/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='lms/lesson_pdfs/', blank=True, null=True)
    
    # Additional resources
    attachments = models.JSONField(default=list, blank=True)
    external_links = models.JSONField(default=list, blank=True)
    
    is_preview = models.BooleanField(default=False, help_text="Can be accessed without enrollment")
    is_published = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'lms_lessons'
        ordering = ['module', 'order']
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
    
    def __str__(self):
        return f"{self.module.course.code} - {self.title}"


class Enrollment(TimeStampedModel):
    """Student Course Enrollment"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('expired', 'Expired'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='lms_enrollments')
    
    enrollment_date = models.DateTimeField(default=timezone.now)
    completion_date = models.DateTimeField(null=True, blank=True)
    
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)
    
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('refunded', 'Refunded'),
        ],
        default='pending'
    )
    
    certificate_issued = models.BooleanField(default=False)
    certificate_number = models.CharField(max_length=100, blank=True, unique=True, null=True)
    
    objects = EnrollmentManager()
    
    class Meta:
        db_table = 'lms_enrollments'
        unique_together = ['course', 'student']
        ordering = ['-enrollment_date']
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['course', 'status']),
        ]
    
    def __str__(self):
        return f"{self.student.user.email} - {self.course.title}"


class LessonProgress(TimeStampedModel):
    """Track student progress on lessons"""
    
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='student_progress')
    
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    
    time_spent_minutes = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'lms_lesson_progress'
        unique_together = ['enrollment', 'lesson']
        ordering = ['enrollment', 'lesson']
    
    def __str__(self):
        return f"{self.enrollment.student.user.email} - {self.lesson.title}"


class Quiz(TimeStampedModel):
    """Quiz/Assessment"""
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    
    passing_score = models.DecimalField(max_digits=5, decimal_places=2, default=60, validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_attempts = models.IntegerField(default=3, validators=[MinValueValidator(1)])
    time_limit_minutes = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    
    is_mandatory = models.BooleanField(default=False)
    show_correct_answers = models.BooleanField(default=True)
    randomize_questions = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'lms_quizzes'
        ordering = ['lesson']
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
    
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class Question(TimeStampedModel):
    """Quiz Question"""
    
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
        ('essay', 'Essay'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    
    points = models.DecimalField(max_digits=5, decimal_places=2, default=1, validators=[MinValueValidator(0)])
    order = models.IntegerField(default=0)
    
    # For multiple choice
    options = models.JSONField(default=list, blank=True, help_text="List of answer options")
    correct_answer = models.TextField(help_text="Correct answer or answer key")
    
    explanation = models.TextField(blank=True)
    
    class Meta:
        db_table = 'lms_questions'
        ordering = ['quiz', 'order']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"


class QuizAttempt(TimeStampedModel):
    """Student Quiz Attempt"""
    
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='quiz_attempts')
    
    attempt_number = models.IntegerField(default=1)
    
    started_at = models.DateTimeField(default=timezone.now)
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_points = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    passed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    
    class Meta:
        db_table = 'lms_quiz_attempts'
        ordering = ['-started_at']
        verbose_name = 'Quiz Attempt'
        verbose_name_plural = 'Quiz Attempts'
    
    def __str__(self):
        return f"{self.enrollment.student.user.email} - {self.quiz.title} (Attempt {self.attempt_number})"


class QuizAnswer(TimeStampedModel):
    """Student Answer to Quiz Question"""
    
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='student_answers')
    
    answer_text = models.TextField()
    is_correct = models.BooleanField(null=True, blank=True)
    points_earned = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    feedback = models.TextField(blank=True)
    
    class Meta:
        db_table = 'lms_quiz_answers'
        unique_together = ['attempt', 'question']
    
    def __str__(self):
        return f"{self.attempt} - {self.question}"


class Assignment(TimeStampedModel):
    """Course Assignment"""
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignments')
    
    title = models.CharField(max_length=300)
    description = models.TextField()
    instructions = models.TextField(blank=True)
    
    max_points = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    
    due_date = models.DateTimeField(null=True, blank=True)
    allow_late_submission = models.BooleanField(default=True)
    late_penalty_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    
    attachment = models.FileField(upload_to='lms/assignment_files/', blank=True, null=True)
    
    class Meta:
        db_table = 'lms_assignments'
        ordering = ['lesson', '-due_date']
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
    
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class AssignmentSubmission(TimeStampedModel):
    """Student Assignment Submission"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('returned', 'Returned'),
    ]
    
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='assignment_submissions')
    
    submission_date = models.DateTimeField(default=timezone.now)
    is_late = models.BooleanField(default=False)
    
    content = models.TextField(blank=True)
    attachment = models.FileField(upload_to='lms/assignment_submissions/%Y/%m/', blank=True, null=True)
    
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_assignments')
    graded_at = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    class Meta:
        db_table = 'lms_assignment_submissions'
        unique_together = ['assignment', 'enrollment']
        ordering = ['-submission_date']
        verbose_name = 'Assignment Submission'
        verbose_name_plural = 'Assignment Submissions'
    
    def __str__(self):
        return f"{self.enrollment.student.user.email} - {self.assignment.title}"


class Discussion(TimeStampedModel):
    """Course Discussion Thread"""
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='discussions')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='discussions')
    
    title = models.CharField(max_length=300)
    content = models.TextField()
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lms_discussions')
    
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    
    views_count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'lms_discussions'
        ordering = ['-is_pinned', '-created_at']
        verbose_name = 'Discussion'
        verbose_name_plural = 'Discussions'
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"


class DiscussionReply(TimeStampedModel):
    """Reply to Discussion Thread"""
    
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='replies')
    parent_reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_replies')
    
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lms_discussion_replies')
    
    is_answer = models.BooleanField(default=False)
    upvotes = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'lms_discussion_replies'
        ordering = ['created_at']
        verbose_name = 'Discussion Reply'
        verbose_name_plural = 'Discussion Replies'
    
    def __str__(self):
        return f"Reply to {self.discussion.title}"


class Certificate(TimeStampedModel):
    """Course Completion Certificate"""
    
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    
    certificate_number = models.CharField(max_length=100, unique=True)
    issue_date = models.DateField(default=timezone.now)
    
    certificate_file = models.FileField(upload_to='lms/certificates/%Y/', blank=True, null=True)
    
    verification_url = models.URLField(blank=True)
    
    class Meta:
        db_table = 'lms_certificates'
        ordering = ['-issue_date']
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'
    
    def __str__(self):
        return f"{self.certificate_number} - {self.enrollment.student.user.email}"
