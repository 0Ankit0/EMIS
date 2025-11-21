"""Email utilities for EMIS"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


class EmailService:
    """Email service for sending various types of emails"""
    
    @staticmethod
    def send_welcome_email(user):
        """Send welcome email to new user"""
        subject = 'Welcome to EMIS'
        
        context = {
            'user': user,
            'login_url': f"{settings.SITE_URL}/auth/login/",
        }
        
        html_message = render_to_string('emails/welcome.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_password_reset_email(user, reset_link):
        """Send password reset email"""
        subject = 'Reset Your Password - EMIS'
        
        context = {
            'user': user,
            'reset_link': reset_link,
        }
        
        html_message = render_to_string('emails/password_reset.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_admission_status_email(application, status):
        """Send admission status update email"""
        subject = f'Admission Application {status.title()} - EMIS'
        
        context = {
            'application': application,
            'status': status,
        }
        
        html_message = render_to_string('emails/admission_status.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [application.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_course_enrollment_email(enrollment):
        """Send course enrollment confirmation email"""
        subject = 'Course Enrollment Confirmation - EMIS'
        
        context = {
            'enrollment': enrollment,
            'student': enrollment.student,
            'course': enrollment.course,
        }
        
        html_message = render_to_string('emails/course_enrollment.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [enrollment.student.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_fee_reminder_email(student, fee_details):
        """Send fee payment reminder email"""
        subject = 'Fee Payment Reminder - EMIS'
        
        context = {
            'student': student,
            'fee_details': fee_details,
        }
        
        html_message = render_to_string('emails/fee_reminder.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [student.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_exam_schedule_email(student, exam):
        """Send exam schedule notification"""
        subject = 'Exam Schedule Notification - EMIS'
        
        context = {
            'student': student,
            'exam': exam,
        }
        
        html_message = render_to_string('emails/exam_schedule.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [student.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_grade_published_email(student, course, grade):
        """Send grade published notification"""
        subject = f'Grade Published for {course.name} - EMIS'
        
        context = {
            'student': student,
            'course': course,
            'grade': grade,
        }
        
        html_message = render_to_string('emails/grade_published.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [student.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_bulk_email(recipients, subject, message, html_message=None):
        """Send bulk email to multiple recipients"""
        if html_message:
            email = EmailMultiAlternatives(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipients
            )
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)
        else:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipients,
                fail_silently=False,
            )
    
    @staticmethod
    def send_custom_email(recipient, subject, template_name, context):
        """Send custom email using template"""
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            html_message=html_message,
            fail_silently=False,
        )
