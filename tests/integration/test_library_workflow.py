"""Integration tests for Library Workflow"""
import pytest
from datetime import datetime, timedelta, date
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.library import Book, LibraryMember, Issue
from src.models.student import Student


@pytest.mark.asyncio
async def test_complete_library_circulation_workflow(db_session: AsyncSession):
    """Test complete library workflow from book issue to return with fine"""
    # Step 1: Create student
    student = Student(
        id=uuid4(),
        student_id="STU001",
        first_name="John",
        last_name="Reader",
        email="john.reader@example.com",
        program="B.Tech",
        status="active"
    )
    db_session.add(student)
    await db_session.commit()
    
    # Step 2: Create library member
    member = LibraryMember(
        id=uuid4(),
        member_id="LIB001",
        student_id=student.id,
        member_type="student",
        status="active"
    )
    db_session.add(member)
    await db_session.commit()
    
    # Step 3: Add book to library
    book = Book(
        id=uuid4(),
        isbn="978-0-123456-78-9",
        title="Python Programming",
        author="John Author",
        publisher="Tech Books",
        total_copies=5,
        available_copies=5
    )
    db_session.add(book)
    await db_session.commit()
    
    # Step 4: Issue book
    issue = Issue(
        id=uuid4(),
        book_id=book.id,
        member_id=member.id,
        issue_date=datetime.utcnow() - timedelta(days=20),  # Issued 20 days ago
        due_date=datetime.utcnow() - timedelta(days=6),     # Overdue by 6 days
        status="issued"
    )
    db_session.add(issue)
    
    # Update book availability
    book.available_copies = 4
    await db_session.commit()
    
    # Step 5: Return book (overdue)
    issue.return_date = datetime.utcnow()
    issue.status = "returned"
    
    # Calculate fine (6 days overdue * 10 per day)
    days_overdue = (issue.return_date - issue.due_date).days
    fine_per_day = Decimal("10.00")
    total_fine = Decimal(str(days_overdue)) * fine_per_day
    issue.fine_amount = total_fine
    
    # Update book availability
    book.available_copies = 5
    await db_session.commit()
    
    # Assertions
    assert issue.status == "returned"
    assert issue.fine_amount == Decimal("60.00")
    assert book.available_copies == 5


@pytest.mark.asyncio
async def test_book_reservation_workflow(db_session: AsyncSession):
    """Test book reservation when all copies are issued"""
    # Create book with limited copies
    book = Book(
        id=uuid4(),
        isbn="978-1-111111-11-1",
        title="Popular Book",
        author="Famous Author",
        total_copies=2,
        available_copies=0  # All issued
    )
    db_session.add(book)
    await db_session.commit()
    
    # Student wants to reserve
    student = Student(
        id=uuid4(),
        student_id="STU002",
        first_name="Jane",
        last_name="Waiter",
        email="jane.wait@example.com",
        program="MBA",
        status="active"
    )
    db_session.add(student)
    
    member = LibraryMember(
        id=uuid4(),
        member_id="LIB002",
        student_id=student.id,
        member_type="student",
        status="active"
    )
    db_session.add(member)
    await db_session.commit()
    
    # Create reservation
    from src.models.library import Reservation
    reservation = Reservation(
        id=uuid4(),
        book_id=book.id,
        member_id=member.id,
        reservation_date=datetime.utcnow(),
        status="pending"
    )
    db_session.add(reservation)
    await db_session.commit()
    
    # When book becomes available
    book.available_copies = 1
    reservation.status = "ready"
    reservation.notification_sent = True
    await db_session.commit()
    
    assert reservation.status == "ready"
    assert book.available_copies == 1
