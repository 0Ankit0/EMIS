"""
LMS Admin Configuration
"""
from django.contrib import admin
from .models import (
    Course, Module, Lesson, Enrollment, LessonProgress,
    Quiz, Question, QuizAttempt, QuizAnswer,
    Assignment, AssignmentSubmission,
    Discussion, DiscussionReply, Certificate
)


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    fields = ['title', 'order', 'duration_minutes', 'is_published']


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ['title', 'content_type', 'order', 'duration_minutes', 'is_published']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'instructor', 'difficulty_level', 'status', 'enrollment_count', 'created_at']
    list_filter = ['status', 'difficulty_level', 'is_free', 'created_at']
    search_fields = ['title', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at', 'enrollment_count']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    inlines = [ModuleInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'code', 'category', 'difficulty_level')
        }),
        ('Description', {
            'fields': ('short_description', 'description', 'prerequisites', 'learning_objectives')
        }),
        ('Instructor & Media', {
            'fields': ('instructor', 'thumbnail', 'intro_video')
        }),
        ('Pricing & Enrollment', {
            'fields': ('price', 'is_free', 'max_enrollments', 'enrollment_count')
        }),
        ('Schedule', {
            'fields': ('duration_hours', 'start_date', 'end_date')
        }),
        ('Status', {
            'fields': ('status', 'publish_date')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration_minutes', 'is_published']
    list_filter = ['is_published', 'course']
    search_fields = ['title', 'course__title']
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'content_type', 'order', 'duration_minutes', 'is_published', 'is_preview']
    list_filter = ['content_type', 'is_published', 'is_preview']
    search_fields = ['title', 'module__title']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrollment_date', 'progress_percentage', 'status', 'certificate_issued']
    list_filter = ['status', 'payment_status', 'certificate_issued', 'enrollment_date']
    search_fields = ['student__user__email', 'course__title']
    readonly_fields = ['enrollment_date', 'completion_date']
    date_hierarchy = 'enrollment_date'


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'lesson', 'is_completed', 'time_spent_minutes', 'last_accessed']
    list_filter = ['is_completed', 'last_accessed']
    search_fields = ['enrollment__student__user__email', 'lesson__title']


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['question_text', 'question_type', 'points', 'order']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'passing_score', 'max_attempts', 'is_mandatory']
    list_filter = ['is_mandatory', 'show_correct_answers']
    search_fields = ['title', 'lesson__title']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_type', 'order', 'points']
    list_filter = ['question_type']
    search_fields = ['question_text', 'quiz__title']


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'quiz', 'attempt_number', 'score', 'passed', 'status', 'submitted_at']
    list_filter = ['status', 'passed', 'started_at']
    search_fields = ['enrollment__student__user__email', 'quiz__title']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'max_points', 'due_date', 'allow_late_submission']
    list_filter = ['allow_late_submission', 'due_date']
    search_fields = ['title', 'lesson__title']


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'enrollment', 'submission_date', 'is_late', 'score', 'status']
    list_filter = ['status', 'is_late', 'submission_date']
    search_fields = ['assignment__title', 'enrollment__student__user__email']


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'created_by', 'views_count', 'is_pinned', 'is_locked', 'created_at']
    list_filter = ['is_pinned', 'is_locked', 'created_at']
    search_fields = ['title', 'content', 'course__title']


@admin.register(DiscussionReply)
class DiscussionReplyAdmin(admin.ModelAdmin):
    list_display = ['discussion', 'created_by', 'is_answer', 'upvotes', 'created_at']
    list_filter = ['is_answer', 'created_at']
    search_fields = ['content', 'discussion__title']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_number', 'enrollment', 'issue_date']
    list_filter = ['issue_date']
    search_fields = ['certificate_number', 'enrollment__student__user__email']
    readonly_fields = ['issue_date']
