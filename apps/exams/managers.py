"""
Exams Custom Managers and QuerySets
"""
from django.db import models
from django.utils import timezone


class ExamQuerySet(models.QuerySet):
    """Custom queryset for Exam"""
    
    def scheduled(self):
        """Get only scheduled exams"""
        return self.filter(status='scheduled')
    
    def ongoing(self):
        """Get only ongoing exams"""
        return self.filter(status='ongoing')
    
    def completed(self):
        """Get only completed exams"""
        return self.filter(status='completed')
    
    def cancelled(self):
        """Get only cancelled exams"""
        return self.filter(status='cancelled')
    
    def by_course(self, course):
        """Get exams for specific course"""
        return self.filter(course=course)
    
    def by_academic_year(self, year):
        """Get exams for specific academic year"""
        return self.filter(academic_year=year)
    
    def by_semester(self, semester):
        """Get exams for specific semester"""
        return self.filter(semester=semester)
    
    def upcoming(self):
        """Get upcoming exams"""
        return self.filter(exam_date__gte=timezone.now().date(), status='scheduled')
    
    def past(self):
        """Get past exams"""
        return self.filter(exam_date__lt=timezone.now().date())


class ExamManager(models.Manager):
    """Custom manager for Exam"""
    
    def get_queryset(self):
        return ExamQuerySet(self.model, using=self._db)
    
    def scheduled(self):
        return self.get_queryset().scheduled()
    
    def ongoing(self):
        return self.get_queryset().ongoing()
    
    def completed(self):
        return self.get_queryset().completed()
    
    def cancelled(self):
        return self.get_queryset().cancelled()
    
    def by_course(self, course):
        return self.get_queryset().by_course(course)
    
    def by_academic_year(self, year):
        return self.get_queryset().by_academic_year(year)
    
    def by_semester(self, semester):
        return self.get_queryset().by_semester(semester)
    
    def upcoming(self):
        return self.get_queryset().upcoming()
    
    def past(self):
        return self.get_queryset().past()


class ExamResultQuerySet(models.QuerySet):
    """Custom queryset for ExamResult"""
    
    def passed(self):
        """Get only passed results"""
        return self.filter(is_passed=True)
    
    def failed(self):
        """Get only failed results"""
        return self.filter(is_passed=False, is_absent=False)
    
    def absent(self):
        """Get only absent results"""
        return self.filter(is_absent=True)
    
    def by_student(self, student):
        """Get results for specific student"""
        return self.filter(student=student)
    
    def by_exam(self, exam):
        """Get results for specific exam"""
        return self.filter(exam=exam)
    
    def by_grade(self, grade):
        """Get results for specific grade"""
        return self.filter(grade=grade)


class ExamResultManager(models.Manager):
    """Custom manager for ExamResult"""
    
    def get_queryset(self):
        return ExamResultQuerySet(self.model, using=self._db)
    
    def passed(self):
        return self.get_queryset().passed()
    
    def failed(self):
        return self.get_queryset().failed()
    
    def absent(self):
        return self.get_queryset().absent()
    
    def by_student(self, student):
        return self.get_queryset().by_student(student)
    
    def by_exam(self, exam):
        return self.get_queryset().by_exam(exam)
    
    def by_grade(self, grade):
        return self.get_queryset().by_grade(grade)
