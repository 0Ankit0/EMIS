from django.db import models
from . import Student
import uuid
from . import BaseModel

class DocumentType(models.TextChoices):
    """Document type choices."""
    ID_PROOF = 'id_proof', 'ID Proof'
    BIRTH_CERTIFICATE = 'birth_cert', 'Birth Certificate'
    ACADEMIC_TRANSCRIPT = 'transcript', 'Academic Transcript'
    PHOTOGRAPH = 'photo', 'Photograph'
    MEDICAL_CERTIFICATE = 'medical', 'Medical Certificate'
    TRANSFER_CERTIFICATE = 'transfer', 'Transfer Certificate'
    OTHER = 'other', 'Other'

class Document(BaseModel):
    """Model representing a document related to a student."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=255, choices=DocumentType.choices)
    file = models.FileField(upload_to='student_documents/')
    is_verified = models.BooleanField(default=False)
    verified_by = models.CharField(max_length=100, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.document_type} for {self.student}"
    
    class Meta: # type: ignore
        db_table = 'student_documents'
        ordering = ['-uploaded_at']