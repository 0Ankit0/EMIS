"""Library service for EMIS."""
from datetime import datetime, date, timedelta
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.library import Book, BookTransaction, BookStatus, TransactionType
from src.models.student import Student
from src.models.employee import Employee
from src.lib.audit import log_audit, AuditAction
from src.lib.logging import get_logger

logger = get_logger(__name__)


class LibraryService:
    """Service for managing library operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_book(
        self,
        isbn: str,
        title: str,
        author: str,
        publisher: Optional[str] = None,
        publication_year: Optional[int] = None,
        category: Optional[str] = None,
        total_copies: int = 1,
        shelf_location: Optional[str] = None,
    ) -> Book:
        """Add a new book to the library."""
        # Check if book with ISBN already exists
        result = await self.db.execute(
            select(Book).where(Book.isbn == isbn)
        )
        existing_book = result.scalar_one_or_none()

        if existing_book:
            # Update total copies
            existing_book.total_copies += total_copies
            existing_book.available_copies += total_copies
            await self.db.commit()
            await self.db.refresh(existing_book)
            
            logger.info(f"Added {total_copies} copies to existing book: {isbn}")
            return existing_book

        book = Book(
            isbn=isbn,
            title=title,
            author=author,
            publisher=publisher,
            publication_year=publication_year,
            category=category,
            total_copies=total_copies,
            available_copies=total_copies,
            shelf_location=shelf_location,
            status=BookStatus.AVAILABLE,
        )

        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)

        await log_audit(
            self.db,
            action=AuditAction.CREATE,
            entity_type="Book",
            entity_id=book.id,
            details={"isbn": isbn, "title": title}
        )

        logger.info(f"Book added to library: {title} (ISBN: {isbn})")
        return book

    async def issue_book(
        self,
        book_id: UUID,
        borrower_id: UUID,
        borrower_type: str,  # 'student' or 'employee'
        due_date: Optional[date] = None,
        issued_by: Optional[UUID] = None,
    ) -> BookTransaction:
        """Issue a book to a borrower."""
        # Verify book exists and is available
        book_result = await self.db.execute(
            select(Book).where(Book.id == book_id)
        )
        book = book_result.scalar_one_or_none()
        
        if not book:
            raise ValueError(f"Book {book_id} not found")

        if book.available_copies <= 0:
            raise ValueError("Book is not available for issue")

        # Verify borrower exists
        if borrower_type == "student":
            borrower_result = await self.db.execute(
                select(Student).where(Student.id == borrower_id)
            )
        else:
            borrower_result = await self.db.execute(
                select(Employee).where(Employee.id == borrower_id)
            )

        if not borrower_result.scalar_one_or_none():
            raise ValueError(f"Borrower {borrower_id} not found")

        # Check if borrower has overdue books
        overdue_result = await self.db.execute(
            select(BookTransaction).where(
                and_(
                    BookTransaction.borrower_id == borrower_id,
                    BookTransaction.transaction_type == TransactionType.ISSUE,
                    BookTransaction.status == "issued",
                    BookTransaction.due_date < date.today()
                )
            )
        )
        if overdue_result.scalar_one_or_none():
            raise ValueError("Borrower has overdue books")

        # Set default due date (14 days from now)
        if not due_date:
            due_date = date.today() + timedelta(days=14)

        # Create transaction
        transaction = BookTransaction(
            book_id=book_id,
            borrower_id=borrower_id,
            borrower_type=borrower_type,
            transaction_type=TransactionType.ISSUE,
            issue_date=date.today(),
            due_date=due_date,
            status="issued",
            issued_by=issued_by,
        )

        self.db.add(transaction)

        # Update book availability
        book.available_copies -= 1
        if book.available_copies == 0:
            book.status = BookStatus.ISSUED

        await self.db.commit()
        await self.db.refresh(transaction)

        await log_audit(
            self.db,
            action=AuditAction.CREATE,
            entity_type="BookTransaction",
            entity_id=transaction.id,
            user_id=borrower_id,
            details={
                "book_id": str(book_id),
                "borrower_type": borrower_type,
                "due_date": due_date.isoformat()
            }
        )

        logger.info(f"Book issued: {book.title} to {borrower_type} {borrower_id}")
        return transaction

    async def return_book(
        self,
        transaction_id: UUID,
        return_date: Optional[date] = None,
        condition_notes: Optional[str] = None,
        fine_amount: Optional[float] = None,
    ) -> BookTransaction:
        """Return a book."""
        result = await self.db.execute(
            select(BookTransaction).where(BookTransaction.id == transaction_id)
        )
        transaction = result.scalar_one_or_none()

        if not transaction:
            raise ValueError(f"Transaction {transaction_id} not found")

        if transaction.status != "issued":
            raise ValueError("Book is not currently issued")

        if not return_date:
            return_date = date.today()

        transaction.return_date = return_date
        transaction.status = "returned"
        transaction.condition_notes = condition_notes

        # Calculate fine if overdue
        if return_date > transaction.due_date:
            days_overdue = (return_date - transaction.due_date).days
            calculated_fine = days_overdue * 5.0  # $5 per day
            transaction.fine_amount = fine_amount or calculated_fine
            logger.info(f"Book returned late. Fine: ${transaction.fine_amount}")

        # Update book availability
        book_result = await self.db.execute(
            select(Book).where(Book.id == transaction.book_id)
        )
        book = book_result.scalar_one_or_none()
        
        if book:
            book.available_copies += 1
            if book.available_copies > 0:
                book.status = BookStatus.AVAILABLE

        await self.db.commit()
        await self.db.refresh(transaction)

        await log_audit(
            self.db,
            action=AuditAction.UPDATE,
            entity_type="BookTransaction",
            entity_id=transaction.id,
            user_id=transaction.borrower_id,
            details={
                "book_id": str(transaction.book_id),
                "return_date": return_date.isoformat(),
                "fine": transaction.fine_amount
            }
        )

        logger.info(f"Book returned: transaction {transaction_id}")
        return transaction

    async def renew_book(self, transaction_id: UUID, new_due_date: Optional[date] = None) -> BookTransaction:
        """Renew a book loan."""
        result = await self.db.execute(
            select(BookTransaction).where(BookTransaction.id == transaction_id)
        )
        transaction = result.scalar_one_or_none()

        if not transaction:
            raise ValueError(f"Transaction {transaction_id} not found")

        if transaction.status != "issued":
            raise ValueError("Book is not currently issued")

        if not new_due_date:
            new_due_date = transaction.due_date + timedelta(days=14)

        transaction.due_date = new_due_date

        await self.db.commit()
        await self.db.refresh(transaction)

        await log_audit(
            self.db,
            action=AuditAction.UPDATE,
            entity_type="BookTransaction",
            entity_id=transaction.id,
            user_id=transaction.borrower_id,
            details={"new_due_date": new_due_date.isoformat()}
        )

        logger.info(f"Book renewed: transaction {transaction_id}")
        return transaction

    async def get_overdue_books(self) -> List[BookTransaction]:
        """Get all overdue book transactions."""
        result = await self.db.execute(
            select(BookTransaction).where(
                and_(
                    BookTransaction.status == "issued",
                    BookTransaction.due_date < date.today()
                )
            )
        )
        return list(result.scalars().all())

    async def get_borrower_history(
        self,
        borrower_id: UUID,
        borrower_type: str
    ) -> List[BookTransaction]:
        """Get borrowing history for a user."""
        result = await self.db.execute(
            select(BookTransaction).where(
                and_(
                    BookTransaction.borrower_id == borrower_id,
                    BookTransaction.borrower_type == borrower_type
                )
            ).order_by(BookTransaction.issue_date.desc())
        )
        return list(result.scalars().all())

    async def search_books(
        self,
        query: str,
        category: Optional[str] = None,
        available_only: bool = False
    ) -> List[Book]:
        """Search books by title, author, or ISBN."""
        filters = [
            or_(
                Book.title.ilike(f"%{query}%"),
                Book.author.ilike(f"%{query}%"),
                Book.isbn.ilike(f"%{query}%")
            )
        ]

        if category:
            filters.append(Book.category == category)

        if available_only:
            filters.append(Book.available_copies > 0)

        result = await self.db.execute(
            select(Book).where(and_(*filters))
        )
        return list(result.scalars().all())
