from django.db import models
from . import Student
import uuid
from . import BaseModel

class Document(BaseModel):
    DOCUMENT_TYPE_CHOICES = [
        ('id_proof', 'ID Proof'),
        ('birth_cert', 'Birth Certificate'),
        ('transcript', 'Academic Transcript'),
        ('photo', 'Photograph'),
        ('medical', 'Medical Certificate'),
        ('transfer', 'Transfer Certificate'),
        ('other', 'Other'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=255, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to='student_documents/')
    is_verified = models.BooleanField(default=False)
    verified_by = models.CharField(max_length=100, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.document_type} for {self.student}"
    
    class Meta: # type: ignore
        db_table = 'student_documents'
        ordering = ['-uploaded_at']