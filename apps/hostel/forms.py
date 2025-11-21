"""Hostel Forms"""
from django import forms
from .models import (
    Hostel, Floor, Room, RoomAllocation, HostelFee, MessMenu,
    VisitorLog, Complaint, OutingRequest, Attendance
)


class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['name', 'code', 'hostel_type', 'address', 'city', 'pincode',
                  'total_floors', 'total_rooms', 'total_capacity', 'warden',
                  'contact_number', 'email', 'amenities', 'facilities',
                  'rules_and_regulations', 'status', 'is_active', 'established_date']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'facilities': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rules_and_regulations': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'established_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = ['hostel', 'floor_number', 'total_rooms', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['hostel', 'floor', 'room_number', 'room_type', 'capacity',
                  'area_sqft', 'has_attached_bathroom', 'has_balcony', 'has_ac',
                  'furniture', 'monthly_rent', 'status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class RoomAllocationForm(forms.ModelForm):
    class Meta:
        model = RoomAllocation
        fields = ['student', 'room', 'bed_number', 'allocation_date', 'academic_year',
                  'semester', 'monthly_rent', 'security_deposit', 'remarks']
        widgets = {
            'allocation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class HostelFeeForm(forms.ModelForm):
    class Meta:
        model = HostelFee
        fields = ['hostel', 'room_type', 'fee_type', 'accommodation_fee', 'mess_fee',
                  'maintenance_fee', 'electricity_charges', 'other_charges',
                  'security_deposit', 'academic_year', 'is_active', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class MessMenuForm(forms.ModelForm):
    class Meta:
        model = MessMenu
        fields = ['hostel', 'day_of_week', 'meal_type', 'menu_items', 'timing',
                  'is_active', 'effective_from']
        widgets = {
            'effective_from': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class VisitorLogForm(forms.ModelForm):
    class Meta:
        model = VisitorLog
        fields = ['hostel', 'student', 'visitor_name', 'visitor_phone',
                  'visitor_id_type', 'visitor_id_number', 'purpose',
                  'purpose_details', 'remarks']
        widgets = {
            'purpose_details': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['hostel', 'room', 'category', 'title', 'description',
                  'priority', 'attachment']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class ComplaintResolutionForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['resolution', 'assigned_to']
        widgets = {
            'resolution': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class OutingRequestForm(forms.ModelForm):
    class Meta:
        model = OutingRequest
        fields = ['hostel', 'out_date', 'out_time', 'expected_return_date',
                  'expected_return_time', 'destination', 'purpose',
                  'parent_contact', 'emergency_contact', 'remarks']
        widgets = {
            'out_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'out_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'expected_return_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expected_return_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'purpose': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        out_date = cleaned_data.get('out_date')
        return_date = cleaned_data.get('expected_return_date')
        
        if out_date and return_date and out_date > return_date:
            raise forms.ValidationError("Return date must be after out date")
        
        return cleaned_data


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['hostel', 'student', 'date', 'status', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
