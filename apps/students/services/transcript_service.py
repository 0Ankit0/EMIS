from typing import Optional, Dict, Any
from decimal import Decimal
from django.utils import timezone
from apps.students.models import Transcript, Student
from apps.courses.models import GradeRecord
from apps.courses.services import GradingService
from apps.core.exceptions import EMISException


class TranscriptService:
    """Service for generating and managing student transcripts"""
    
    @staticmethod
    def generate_transcript(
        student_id: str,
        transcript_type: str = 'unofficial',
        semester: Optional[str] = None,
        academic_year: Optional[str] = None,
        generated_by_id: Optional[str] = None
    ) -> Transcript:
        """
        Generate a transcript for a student (includes only finalized grades)
        
        Args:
            student_id: Student ID
            transcript_type: Type of transcript (official, unofficial, interim)
            semester: Optional semester filter
            academic_year: Optional academic year filter
            generated_by_id: ID of user generating the transcript
            
        Returns:
            Transcript object
        """
        # Verify student exists
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise EMISException(
                code="STUDENTS_001",
                message=f"Student {student_id} not found"
            )
        
        # Get finalized grade records
        queryset = GradeRecord.objects.filter(
            student_id=student_id,
            finalized=True
        ).select_related('course')
        
        if semester:
            queryset = queryset.filter(semester=semester)
        
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        
        grade_records = list(queryset.order_by('academic_year', 'semester', 'course__code'))
        
        # Build grade records snapshot
        grade_records_snapshot = {
            'grades': [
                {
                    'course_code': gr.course.code,
                    'course_title': gr.course.title,
                    'credits': gr.course.credits,
                    'grade_value': float(gr.grade_value),
                    'grade_letter': gr.grade_letter,
                    'grade_points': float(gr.grade_points),
                    'semester': gr.semester,
                    'academic_year': gr.academic_year,
                    'finalized_at': gr.finalized_at.isoformat() if gr.finalized_at else None,
                }
                for gr in grade_records
            ]
        }
        
        # Calculate academic summary
        total_credits_attempted = sum(gr.course.credits for gr in grade_records)
        
        # Credits earned (passing grades only - >= D which is 60+)
        total_credits_earned = sum(
            gr.course.credits for gr in grade_records
            if gr.grade_value >= 60
        )
        
        # Calculate cumulative GPA
        cumulative_gpa = GradingService.calculate_gpa(
            student_id=student_id,
            semester=semester,
            academic_year=academic_year
        ) or Decimal('0.00')
        
        # Create transcript
        transcript = Transcript.objects.create(
            student=student,
            grade_records_snapshot=grade_records_snapshot,
            total_credits_attempted=total_credits_attempted,
            total_credits_earned=total_credits_earned,
            cumulative_gpa=cumulative_gpa,
            transcript_type=transcript_type,
            semester=semester or '',
            academic_year=academic_year or '',
            generated_by_id=generated_by_id,
        )
        
        return transcript
    
    @staticmethod
    def get_transcript(transcript_id: str) -> Optional[Transcript]:
        """Get a transcript by ID"""
        try:
            return Transcript.objects.select_related('student', 'generated_by').get(id=transcript_id)
        except Transcript.DoesNotExist:
            return None
    
    @staticmethod
    def list_student_transcripts(student_id: str) -> list:
        """List all transcripts for a student"""
        return list(
            Transcript.objects.filter(student_id=student_id)
            .select_related('generated_by')
            .order_by('-generated_at')
        )
    
    @staticmethod
    def certify_transcript(
        transcript_id: str,
        certified_by_id: str
    ) -> Optional[Transcript]:
        """
        Certify a transcript (make it official)
        
        Args:
            transcript_id: Transcript ID
            certified_by_id: ID of user certifying the transcript
            
        Returns:
            Updated Transcript object or None
        """
        try:
            transcript = Transcript.objects.get(id=transcript_id)
            
            if transcript.is_certified:
                raise EMISException(
                    code="STUDENTS_002",
                    message="Transcript is already certified"
                )
            
            transcript.is_certified = True
            transcript.certification_date = timezone.now()
            transcript.transcript_type = 'official'
            transcript.save()
            
            return transcript
        except Transcript.DoesNotExist:
            return None
    
    @staticmethod
    def get_latest_transcript(
        student_id: str,
        transcript_type: Optional[str] = None
    ) -> Optional[Transcript]:
        """Get the most recent transcript for a student"""
        queryset = Transcript.objects.filter(student_id=student_id)
        
        if transcript_type:
            queryset = queryset.filter(transcript_type=transcript_type)
        
        return queryset.order_by('-generated_at').first()
    
    @staticmethod
    def get_transcript_summary(student_id: str) -> Dict[str, Any]:
        """
        Get a summary of student's academic record without generating a full transcript
        
        Returns:
            Dict with credits, GPA, and grade summary
        """
        # Verify student exists
        try:
            Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise EMISException(
                code="STUDENTS_001",
                message=f"Student {student_id} not found"
            )
        
        # Get finalized grade records
        grade_records = GradeRecord.objects.filter(
            student_id=student_id,
            finalized=True
        ).select_related('course')
        
        total_credits_attempted = sum(gr.course.credits for gr in grade_records)
        total_credits_earned = sum(
            gr.course.credits for gr in grade_records
            if gr.grade_value >= 60
        )
        
        cumulative_gpa = GradingService.calculate_gpa(student_id=student_id)
        
        # Count courses by status
        courses_completed = grade_records.filter(grade_value__gte=60).count()
        courses_failed = grade_records.filter(grade_value__lt=60).count()
        
        return {
            'student_id': student_id,
            'total_credits_attempted': total_credits_attempted,
            'total_credits_earned': total_credits_earned,
            'cumulative_gpa': float(cumulative_gpa) if cumulative_gpa else 0.00,
            'courses_completed': courses_completed,
            'courses_failed': courses_failed,
            'total_courses': grade_records.count(),
        }
