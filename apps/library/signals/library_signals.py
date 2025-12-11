"""
Library Signals
"""
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from ..models import Book, BookIssue, LibraryMember

@receiver(post_save, sender=BookIssue)
def book_issue_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for BookIssue post_save
    """
    if created:
        # Book already issued in the form save, but we can add logging here
        pass
    else:
        # Check if status changed to returned
        if instance.status == 'returned' and instance.return_date:
            # Update book availability
            instance.book.return_book()

@receiver(pre_delete, sender=BookIssue)
def book_issue_pre_delete(sender, instance, **kwargs):
    """
    Signal handler for BookIssue pre_delete
    """
    # Return the book before deleting the issue record
    if instance.status == 'issued':
        instance.book.return_book()

@receiver(pre_save, sender=BookIssue)
def check_overdue_status(sender, instance, **kwargs):
    """
    Update status to overdue if past due date
    """
    if instance.pk:
        if instance.is_overdue and instance.status == 'issued':
            instance.status = 'overdue'
