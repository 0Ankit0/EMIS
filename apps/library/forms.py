"""
Library Forms
"""
from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Book, BookIssue, LibraryMember


class BookForm(forms.ModelForm):
    """
    Form for creating and updating books
    """
    class Meta:
        model = Book
        fields = [
            'isbn', 'title', 'author', 'publisher', 'publication_year', 'edition',
            'language', 'pages', 'description', 'category', 'total_copies',
            'available_copies', 'price', 'rack_number', 'shelf_number', 'floor',
            'status', 'cover_image'
        ]
        widgets = {
            'isbn': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter ISBN'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter book title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter author name'
            }),
            'publisher': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter publisher'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter year'
            }),
            'edition': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter edition'
            }),
            'language': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter language'
            }),
            'pages': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Number of pages'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter description',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'total_copies': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'available_copies': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'step': '0.01'
            }),
            'rack_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'shelf_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'floor': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
        }
    
    def clean_isbn(self):
        """Validate ISBN field"""
        isbn = self.cleaned_data.get('isbn')
        if isbn:
            isbn = isbn.strip().replace('-', '')
            if not (len(isbn) == 10 or len(isbn) == 13):
                raise forms.ValidationError("ISBN must be 10 or 13 characters long")
        return isbn
    
    def clean(self):
        cleaned_data = super().clean()
        total_copies = cleaned_data.get('total_copies')
        available_copies = cleaned_data.get('available_copies')
        
        if total_copies and available_copies:
            if available_copies > total_copies:
                raise forms.ValidationError("Available copies cannot exceed total copies")
        
        return cleaned_data


class BookIssueForm(forms.ModelForm):
    """
    Form for issuing books
    """
    class Meta:
        model = BookIssue
        fields = ['book', 'student', 'faculty', 'issue_date', 'due_date', 'notes']
        widgets = {
            'book': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'student': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'faculty': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'issue_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'type': 'date'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'rows': 3
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.available()
        self.fields['student'].required = False
        self.fields['faculty'].required = False
        
        if not self.instance.pk:
            self.fields['issue_date'].initial = timezone.now().date()
            self.fields['due_date'].initial = timezone.now().date() + timedelta(days=14)
    
    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        faculty = cleaned_data.get('faculty')
        book = cleaned_data.get('book')
        
        if not student and not faculty:
            raise forms.ValidationError("Either student or faculty must be selected")
        
        if student and faculty:
            raise forms.ValidationError("Cannot issue to both student and faculty")
        
        if book and not book.is_available:
            raise forms.ValidationError("This book is not available for issue")
        
        return cleaned_data


class BookReturnForm(forms.ModelForm):
    """
    Form for returning books
    """
    class Meta:
        model = BookIssue
        fields = ['return_date', 'fine_amount', 'fine_paid', 'notes']
        widgets = {
            'return_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'type': 'date'
            }),
            'fine_amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'step': '0.01',
                'readonly': True
            }),
            'fine_paid': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'rows': 3
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['return_date'].initial = timezone.now().date()
        
        if self.instance and self.instance.pk:
            self.instance.calculate_fine()
            self.fields['fine_amount'].initial = self.instance.fine_amount


class LibraryMemberForm(forms.ModelForm):
    """
    Form for library membership
    """
    class Meta:
        model = LibraryMember
        fields = ['student', 'faculty', 'member_id', 'membership_date', 'expiry_date', 'status', 'max_books_allowed', 'notes']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'faculty': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'member_id': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter member ID'
            }),
            'membership_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'type': 'date'
            }),
            'expiry_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'max_books_allowed': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'rows': 3
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].required = False
        self.fields['faculty'].required = False
        
        if not self.instance.pk:
            self.fields['membership_date'].initial = timezone.now().date()
            self.fields['expiry_date'].initial = timezone.now().date() + timedelta(days=365)
    
    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        faculty = cleaned_data.get('faculty')
        
        if not student and not faculty:
            raise forms.ValidationError("Either student or faculty must be selected")
        
        if student and faculty:
            raise forms.ValidationError("Cannot assign membership to both student and faculty")
        
        return cleaned_data


class BookSearchForm(forms.Form):
    """
    Form for searching books
    """
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Search by title, author, or ISBN...'
        })
    )
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Categories')] + list(Book._meta.get_field('category').choices),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Status')] + list(Book._meta.get_field('status').choices),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
        })
    )
