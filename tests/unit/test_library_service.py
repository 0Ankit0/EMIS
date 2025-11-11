"""Unit tests for LibraryService"""
import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.library_service import LibraryService
from src.models.library import Book, LibraryMember, Issue


@pytest.fixture
def library_service():
    """Create library service instance"""
    return LibraryService()


@pytest.fixture
async def sample_book(db_session: AsyncSession) -> Book:
    """Create a sample book for testing"""
    book = Book(
        id=uuid4(),
        isbn="978-0-123456-78-9",
        title="Test Book",
        author="Test Author",
        publisher="Test Publisher",
        category="Fiction",
        total_copies=5,
        available_copies=5,
        shelf_location="A1"
    )
    db_session.add(book)
    await db_session.commit()
    await db_session.refresh(book)
    return book


@pytest.fixture
async def sample_member(db_session: AsyncSession) -> LibraryMember:
    """Create a sample library member for testing"""
    member = Member(
        id=uuid4(),
        member_id="MEM001",
        name="Test Member",
        email="member@example.com",
        phone="1234567890",
        member_type="student",
        status="active"
    )
    db_session.add(member)
    await db_session.commit()
    await db_session.refresh(member)
    return member


class TestLibraryService:
    """Test cases for LibraryService"""

    @pytest.mark.asyncio
    async def test_add_book(
        self, db_session: AsyncSession, library_service: LibraryService
    ):
        """Test adding a new book to the library"""
        book_data = {
            "isbn": "978-1-234567-89-0",
            "title": "Python Programming",
            "author": "John Doe",
            "publisher": "Tech Books",
            "category": "Programming",
            "total_copies": 3
        }

        book = await library_service.add_book(db_session, book_data)

        assert book is not None
        assert book.isbn == "978-1-234567-89-0"
        assert book.title == "Python Programming"
        assert book.total_copies == 3
        assert book.available_copies == 3

    @pytest.mark.asyncio
    async def test_get_book_by_isbn(
        self, db_session: AsyncSession, library_service: LibraryService, sample_book: Book
    ):
        """Test retrieving a book by ISBN"""
        book = await library_service.get_book_by_isbn(
            db_session, "978-0-123456-78-9"
        )

        assert book is not None
        assert book.isbn == "978-0-123456-78-9"
        assert book.title == "Test Book"

    @pytest.mark.asyncio
    async def test_search_books(
        self, db_session: AsyncSession, library_service: LibraryService, sample_book: Book
    ):
        """Test searching books by title or author"""
        books = await library_service.search_books(db_session, "Test")

        assert len(books) >= 1
        assert any(b.title == "Test Book" for b in books)

    @pytest.mark.asyncio
    async def test_issue_book(
        self,
        db_session: AsyncSession,
        library_service: LibraryService,
        sample_book: Book,
        sample_member: LibraryMember
    ):
        """Test issuing a book to a member"""
        issue = await library_service.issue_book(
            db_session,
            book_id=sample_book.id,
            member_id=sample_member.id,
            due_date=datetime.utcnow() + timedelta(days=14)
        )

        assert issue is not None
        assert issue.book_id == sample_book.id
        assert issue.member_id == sample_member.id
        assert issue.status == "issued"

        # Check available copies decreased
        updated_book = await library_service.get_book_by_id(db_session, sample_book.id)
        assert updated_book.available_copies == 4

    @pytest.mark.asyncio
    async def test_return_book(
        self,
        db_session: AsyncSession,
        library_service: LibraryService,
        sample_book: Book,
        sample_member: LibraryMember
    ):
        """Test returning a book"""
        # First issue the book
        issue = await library_service.issue_book(
            db_session,
            book_id=sample_book.id,
            member_id=sample_member.id,
            due_date=datetime.utcnow() + timedelta(days=14)
        )

        # Then return it
        returned_issue = await library_service.return_book(
            db_session, issue.id
        )

        assert returned_issue is not None
        assert returned_issue.status == "returned"
        assert returned_issue.return_date is not None

        # Check available copies increased back
        updated_book = await library_service.get_book_by_id(db_session, sample_book.id)
        assert updated_book.available_copies == 5

    @pytest.mark.asyncio
    async def test_issue_book_no_copies(
        self,
        db_session: AsyncSession,
        library_service: LibraryService,
        sample_book: Book,
        sample_member: LibraryMember
    ):
        """Test issuing a book when no copies are available"""
        # Set available copies to 0
        sample_book.available_copies = 0
        db_session.add(sample_book)
        await db_session.commit()

        with pytest.raises(Exception):  # Should raise exception
            await library_service.issue_book(
                db_session,
                book_id=sample_book.id,
                member_id=sample_member.id,
                due_date=datetime.utcnow() + timedelta(days=14)
            )

    @pytest.mark.asyncio
    async def test_calculate_fine(
        self,
        db_session: AsyncSession,
        library_service: LibraryService
    ):
        """Test fine calculation for overdue books"""
        # Book overdue by 5 days
        issue_date = datetime.utcnow() - timedelta(days=19)
        due_date = datetime.utcnow() - timedelta(days=5)
        return_date = datetime.utcnow()

        fine = library_service.calculate_fine(
            issue_date=issue_date,
            due_date=due_date,
            return_date=return_date,
            daily_fine=10.0
        )

        assert fine == 50.0  # 5 days * 10.0

    @pytest.mark.asyncio
    async def test_get_overdue_books(
        self,
        db_session: AsyncSession,
        library_service: LibraryService,
        sample_book: Book,
        sample_member: LibraryMember
    ):
        """Test getting overdue books"""
        # Issue book with past due date
        issue = await library_service.issue_book(
            db_session,
            book_id=sample_book.id,
            member_id=sample_member.id,
            due_date=datetime.utcnow() - timedelta(days=5)  # Overdue
        )

        overdue_books = await library_service.get_overdue_books(db_session)

        assert len(overdue_books) >= 1
        assert any(i.id == issue.id for i in overdue_books)

    @pytest.mark.asyncio
    async def test_get_member_borrowed_books(
        self,
        db_session: AsyncSession,
        library_service: LibraryService,
        sample_book: Book,
        sample_member: LibraryMember
    ):
        """Test getting books borrowed by a member"""
        # Issue a book
        await library_service.issue_book(
            db_session,
            book_id=sample_book.id,
            member_id=sample_member.id,
            due_date=datetime.utcnow() + timedelta(days=14)
        )

        borrowed_books = await library_service.get_member_borrowed_books(
            db_session, sample_member.id
        )

        assert len(borrowed_books) >= 1
        assert any(i.book_id == sample_book.id for i in borrowed_books)

    @pytest.mark.asyncio
    async def test_update_book_copies(
        self,
        db_session: AsyncSession,
        library_service: LibraryService,
        sample_book: Book
    ):
        """Test updating book copies"""
        updated_book = await library_service.update_book_copies(
            db_session,
            book_id=sample_book.id,
            total_copies=10
        )

        assert updated_book is not None
        assert updated_book.total_copies == 10
