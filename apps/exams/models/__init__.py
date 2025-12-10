
# Modularized exams models
from .exam import Exam
from .exam_result import ExamResult
    
    def get_percentage(self):
        """Get percentage scored"""
        if self.is_absent:
            return 0
        return (float(self.marks_obtained) / self.exam.total_marks) * 100


class ExamSchedule(TimeStampedModel):
    """
    Exam schedule for organizing multiple exams
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    academic_year = models.CharField(max_length=20)
    semester = models.CharField(
        max_length=20,
        choices=[
            ('fall', 'Fall'),
            ('spring', 'Spring'),
            ('summer', 'Summer'),
        ]
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'exam_schedules'
        ordering = ['-start_date']
        verbose_name = 'Exam Schedule'
        verbose_name_plural = 'Exam Schedules'
    
    def __str__(self):
        return f"{self.name} - {self.academic_year} ({self.semester})"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('exams:schedule_detail', kwargs={'pk': self.pk})
