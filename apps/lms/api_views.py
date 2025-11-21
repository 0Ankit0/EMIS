"""
LMS API Views - REST API endpoints for Learning Management System
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg
from django.utils import timezone

from .models import (
    Course, Module, Lesson, Enrollment, LessonProgress,
    Quiz, Question, QuizAttempt, Assignment, AssignmentSubmission,
    Discussion, DiscussionReply, Certificate
)
from .serializers import (
    CourseListSerializer, CourseDetailSerializer, ModuleSerializer,
    LessonSerializer, EnrollmentSerializer, LessonProgressSerializer,
    QuizSerializer, QuestionSerializer, QuizAttemptSerializer,
    AssignmentSerializer, AssignmentSubmissionSerializer,
    DiscussionSerializer, DiscussionReplySerializer, CertificateSerializer
)
from .filters import CourseFilter, EnrollmentFilter, ModuleFilter, LessonFilter
from .permissions import IsLmsOwner, CanLmsManage


class CourseViewSet(viewsets.ModelViewSet):
    """API endpoint for courses"""
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['title', 'description', 'code', 'category']
    ordering_fields = ['created_at', 'title', 'enrollment_count', 'price']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer
    
    def get_queryset(self):
        queryset = Course.objects.select_related('instructor')
        
        if self.action == 'list':
            # Only show published courses to non-staff
            if not self.request.user.is_staff:
                queryset = queryset.filter(status='published')
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Enroll in a course"""
        course = self.get_object()
        
        if not hasattr(request.user, 'student_profile'):
            return Response({'error': 'Only students can enroll'}, status=status.HTTP_403_FORBIDDEN)
        
        student = request.user.student_profile
        
        # Check if already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            return Response({'error': 'Already enrolled'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if course is full
        if course.is_full:
            return Response({'error': 'Course is full'}, status=status.HTTP_400_BAD_REQUEST)
        
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
        
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def modules(self, request, pk=None):
        """Get course modules"""
        course = self.get_object()
        modules = course.modules.filter(is_published=True)
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data)


class ModuleViewSet(viewsets.ModelViewSet):
    """API endpoint for modules"""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ModuleFilter
    ordering_fields = ['order', 'created_at']
    
    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        """Get module lessons"""
        module = self.get_object()
        lessons = module.lessons.filter(is_published=True)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class LessonViewSet(viewsets.ModelViewSet):
    """API endpoint for lessons"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = LessonFilter
    ordering_fields = ['order', 'created_at']


class EnrollmentViewSet(viewsets.ModelViewSet):
    """API endpoint for enrollments"""
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EnrollmentFilter
    ordering_fields = ['enrollment_date', 'progress_percentage']
    
    def get_queryset(self):
        queryset = Enrollment.objects.select_related('student__user', 'course')
        
        # Filter by student if not staff
        if not self.request.user.is_staff and hasattr(self.request.user, 'student_profile'):
            queryset = queryset.filter(student=self.request.user.student_profile)
        
        return queryset


class LessonProgressViewSet(viewsets.ModelViewSet):
    """API endpoint for lesson progress"""
    queryset = LessonProgress.objects.all()
    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        """Mark lesson as complete"""
        progress = self.get_object()
        progress.is_completed = True
        progress.completion_date = timezone.now()
        progress.save()
        
        serializer = self.get_serializer(progress)
        return Response(serializer.data)


class QuizViewSet(viewsets.ModelViewSet):
    """API endpoint for quizzes"""
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """Get quiz questions"""
        quiz = self.get_object()
        questions = quiz.questions.all().order_by('order')
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class QuizAttemptViewSet(viewsets.ModelViewSet):
    """API endpoint for quiz attempts"""
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = QuizAttempt.objects.select_related('quiz', 'enrollment')
        
        # Filter by student if not staff
        if not self.request.user.is_staff and hasattr(self.request.user, 'student_profile'):
            queryset = queryset.filter(enrollment__student=self.request.user.student_profile)
        
        return queryset


class AssignmentViewSet(viewsets.ModelViewSet):
    """API endpoint for assignments"""
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    """API endpoint for assignment submissions"""
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = AssignmentSubmission.objects.select_related('assignment', 'enrollment')
        
        # Filter by student if not staff
        if not self.request.user.is_staff and hasattr(self.request.user, 'student_profile'):
            queryset = queryset.filter(enrollment__student=self.request.user.student_profile)
        
        return queryset


class DiscussionViewSet(viewsets.ModelViewSet):
    """API endpoint for discussions"""
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        """Get discussion replies"""
        discussion = self.get_object()
        replies = discussion.replies.all().order_by('created_at')
        serializer = DiscussionReplySerializer(replies, many=True)
        return Response(serializer.data)


class DiscussionReplyViewSet(viewsets.ModelViewSet):
    """API endpoint for discussion replies"""
    queryset = DiscussionReply.objects.all()
    serializer_class = DiscussionReplySerializer
    permission_classes = [IsAuthenticated]


class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for certificates (read-only)"""
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Certificate.objects.select_related('enrollment__student__user', 'enrollment__course')
        
        # Filter by student if not staff
        if not self.request.user.is_staff and hasattr(self.request.user, 'student_profile'):
            queryset = queryset.filter(enrollment__student=self.request.user.student_profile)
        
        return queryset
