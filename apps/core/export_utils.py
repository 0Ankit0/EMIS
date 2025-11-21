"""Export utilities for CSV and PDF generation"""
import csv
import io
from datetime import datetime
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas


class CSVExporter:
    """CSV Export utility"""
    
    @staticmethod
    def export_students(students):
        """Export students to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="students_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Student ID', 'First Name', 'Last Name', 'Email', 
            'Phone', 'Date of Birth', 'Gender', 'Program', 
            'Year', 'Status', 'Enrollment Date'
        ])
        
        for student in students:
            writer.writerow([
                student.student_id or '',
                student.first_name,
                student.last_name,
                student.email,
                student.phone or '',
                student.date_of_birth.strftime('%Y-%m-%d') if student.date_of_birth else '',
                student.gender or '',
                student.program or '',
                student.year or '',
                'Active' if student.is_active else 'Inactive',
                student.created_at.strftime('%Y-%m-%d') if student.created_at else ''
            ])
        
        return response
    
    @staticmethod
    def export_courses(courses):
        """Export courses to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="courses_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Course Code', 'Course Name', 'Credits', 
            'Department', 'Instructor', 'Status'
        ])
        
        for course in courses:
            writer.writerow([
                course.course_code,
                course.name,
                course.credits,
                course.department or '',
                str(course.instructor) if hasattr(course, 'instructor') and course.instructor else '',
                'Active' if course.is_active else 'Inactive'
            ])
        
        return response
    
    @staticmethod
    def export_faculty(faculty_members):
        """Export faculty to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="faculty_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Faculty ID', 'First Name', 'Last Name', 'Email',
            'Phone', 'Department', 'Designation', 'Status'
        ])
        
        for faculty in faculty_members:
            writer.writerow([
                faculty.employee_id or '',
                faculty.first_name,
                faculty.last_name,
                faculty.email,
                faculty.phone or '',
                faculty.department or '',
                faculty.designation or '',
                'Active' if faculty.is_active else 'Inactive'
            ])
        
        return response
    
    @staticmethod
    def export_generic(queryset, fields, filename='export'):
        """Generic CSV export"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        
        # Write header
        headers = [field.replace('_', ' ').title() for field in fields]
        writer.writerow(headers)
        
        # Write data
        for obj in queryset:
            row = []
            for field in fields:
                value = getattr(obj, field, '')
                if hasattr(value, 'strftime'):
                    value = value.strftime('%Y-%m-%d')
                row.append(str(value) if value else '')
            writer.writerow(row)
        
        return response


class PDFExporter:
    """PDF Export utility"""
    
    def __init__(self, title='EMIS Report'):
        self.title = title
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup custom styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
        ))
    
    def export_students(self, students):
        """Export students to PDF"""
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="students_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []
        
        # Title
        title = Paragraph(f"<b>Student Report</b>", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Subtitle with date
        subtitle = Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['Normal']
        )
        elements.append(subtitle)
        elements.append(Spacer(1, 20))
        
        # Summary
        summary_text = f"Total Students: <b>{students.count()}</b>"
        summary = Paragraph(summary_text, self.styles['CustomHeading'])
        elements.append(summary)
        elements.append(Spacer(1, 20))
        
        # Table data
        data = [['ID', 'Name', 'Email', 'Program', 'Year', 'Status']]
        
        for student in students:
            data.append([
                student.student_id or 'N/A',
                f"{student.first_name} {student.last_name}",
                student.email,
                student.program or 'N/A',
                str(student.year) if student.year else 'N/A',
                'Active' if student.is_active else 'Inactive'
            ])
        
        # Create table
        table = Table(data, colWidths=[1*inch, 1.8*inch, 2*inch, 1.2*inch, 0.7*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ]))
        
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        return response
    
    def export_courses(self, courses):
        """Export courses to PDF"""
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="courses_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []
        
        # Title
        title = Paragraph(f"<b>Course Report</b>", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Date
        subtitle = Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['Normal']
        )
        elements.append(subtitle)
        elements.append(Spacer(1, 20))
        
        # Summary
        summary_text = f"Total Courses: <b>{courses.count()}</b>"
        summary = Paragraph(summary_text, self.styles['CustomHeading'])
        elements.append(summary)
        elements.append(Spacer(1, 20))
        
        # Table
        data = [['Code', 'Course Name', 'Credits', 'Department', 'Status']]
        
        for course in courses:
            data.append([
                course.course_code,
                course.name[:40] + '...' if len(course.name) > 40 else course.name,
                str(course.credits),
                course.department or 'N/A',
                'Active' if course.is_active else 'Inactive'
            ])
        
        table = Table(data, colWidths=[1*inch, 3*inch, 0.8*inch, 1.5*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ]))
        
        elements.append(table)
        doc.build(elements)
        return response
    
    def export_generic_table(self, title, headers, data, filename='report'):
        """Generic table PDF export"""
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []
        
        # Title
        title_para = Paragraph(f"<b>{title}</b>", self.styles['CustomTitle'])
        elements.append(title_para)
        elements.append(Spacer(1, 12))
        
        # Date
        subtitle = Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['Normal']
        )
        elements.append(subtitle)
        elements.append(Spacer(1, 20))
        
        # Table
        table_data = [headers] + data
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ]))
        
        elements.append(table)
        doc.build(elements)
        return response
