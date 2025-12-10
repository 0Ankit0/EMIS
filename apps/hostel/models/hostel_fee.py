from django.db import models
from apps.core.models import TimeStampedModel
from .room import Room

class HostelFee(TimeStampedModel):
    """Hostel Fee Structure"""
    class FeeType(models.TextChoices):
        MONTHLY = 'monthly', 'Monthly'
        SEMESTER = 'semester', 'Semester'
        ANNUAL = 'annual', 'Annual'
    
    hostel = models.ForeignKey('hostel.Hostel', on_delete=models.CASCADE, related_name='fee_structures')
    room_type = models.CharField(max_length=20, choices=Room.RoomType.choices)
    fee_type = models.CharField(max_length=20, choices=FeeType.choices, default=FeeType.MONTHLY)
    accommodation_fee = models.DecimalField(max_digits=10, decimal_places=2, validators=[models.Min(0)])
    mess_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[models.Min(0)])
    maintenance_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[models.Min(0)])
    electricity_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[models.Min(0)])
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[models.Min(0)])
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, validators=[models.Min(0)])
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[models.Min(0)])
    academic_year = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hostel_fees'
        ordering = ['-created_at']
        verbose_name = 'Hostel Fee'
        verbose_name_plural = 'Hostel Fees'
    
    def __str__(self):
        return f"{self.hostel.name} - {self.room_type} ({self.academic_year})"
    
    def save(self, *args, **kwargs):
        self.total_fee = (
            self.accommodation_fee + self.mess_fee + self.maintenance_fee +
            self.electricity_charges + self.other_charges
        )
        super().save(*args, **kwargs)

