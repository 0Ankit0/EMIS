"""Unit tests for StudentService"""
import pytest
from datetime import date, datetime
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.student_service import StudentService
from src.models.student import Student


@pytest.fixture
def student_service():
    """Create student service instance"""
    return StudentService()


@pytest.fixture
async def sample_student(db_session: AsyncSession) -> Student:
    """Create a sample student for testing"""
    student = Student(
        id=uuid4(),
        student_id="STU001",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        date_of_birth=date(2000, 1, 1),
        gender="male",
        blood_group="O+",
        admission_date=datetime.utcnow(),
        program="B.Tech",
        status="active"
    )
    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)
    return student


class TestStudentService:
    """Test cases for StudentService"""

    @pytest.mark.asyncio
    async def test_create_student(
        self, db_session: AsyncSession, student_service: StudentService
    ):
        """Test creating a new student"""
        student_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "phone": "9876543210",
            "date_of_birth": date(2001, 5, 15),
            "gender": "female",
            "program": "B.Tech"
        }

        student = await student_service.create_student(db_session, student_data)

        assert student is not None
        assert student.first_name == "Jane"
        assert student.last_name == "Smith"
        assert student.email == "jane.smith@example.com"
        assert student.student_id is not None
        assert student.status == "active"

    @pytest.mark.asyncio
    async def test_get_student_by_id(
        self, db_session: AsyncSession, student_service: StudentService, sample_student: Student
    ):
        """Test retrieving a student by ID"""
        student = await student_service.get_student_by_id(db_session, sample_student.id)

        assert student is not None
        assert student.id == sample_student.id
        assert student.first_name == "John"
        assert student.email == "john.doe@example.com"

    @pytest.mark.asyncio
    async def test_get_student_by_email(
        self, db_session: AsyncSession, student_service: StudentService, sample_student: Student
    ):
        """Test retrieving a student by email"""
        student = await student_service.get_student_by_email(
            db_session, "john.doe@example.com"
        )

        assert student is not None
        assert student.email == "john.doe@example.com"
        assert student.first_name == "John"

    @pytest.mark.asyncio
    async def test_get_student_not_found(
        self, db_session: AsyncSession, student_service: StudentService
    ):
        """Test retrieving a non-existent student"""
        student = await student_service.get_student_by_id(db_session, uuid4())

        assert student is None

    @pytest.mark.asyncio
    async def test_update_student(
        self, db_session: AsyncSession, student_service: StudentService, sample_student: Student
    ):
        """Test updating a student"""
        update_data = {
            "phone": "9999999999",
            "email": "john.updated@example.com"
        }

        updated_student = await student_service.update_student(
            db_session, sample_student.id, update_data
        )

        assert updated_student is not None
        assert updated_student.phone == "9999999999"
        assert updated_student.email == "john.updated@example.com"
        assert updated_student.first_name == "John"  # Unchanged

    @pytest.mark.asyncio
    async def test_delete_student(
        self, db_session: AsyncSession, student_service: StudentService, sample_student: Student
    ):
        """Test deleting a student"""
        result = await student_service.delete_student(db_session, sample_student.id)

        assert result is True

        # Verify student is deleted
        deleted_student = await student_service.get_student_by_id(
            db_session, sample_student.id
        )
        assert deleted_student is None

    @pytest.mark.asyncio
    async def test_list_students(
        self, db_session: AsyncSession, student_service: StudentService, sample_student: Student
    ):
        """Test listing students with pagination"""
        students, total = await student_service.list_students(
            db_session, skip=0, limit=10
        )

        assert total >= 1
        assert len(students) >= 1
        assert any(s.id == sample_student.id for s in students)

    @pytest.mark.asyncio
    async def test_search_students(
        self, db_session: AsyncSession, student_service: StudentService, sample_student: Student
    ):
        """Test searching students"""
        students = await student_service.search_students(db_session, query="John")

        assert len(students) >= 1
        assert any(s.first_name == "John" for s in students)

    @pytest.mark.asyncio
    async def test_get_students_by_program(
        self, db_session: AsyncSession, student_service: StudentService, sample_student: Student
    ):
        """Test getting students by program"""
        students = await student_service.get_students_by_program(db_session, "B.Tech")

        assert len(students) >= 1
        assert all(s.program == "B.Tech" for s in students)

    @pytest.mark.asyncio
    async def test_generate_student_id(
        self, db_session: AsyncSession, student_service: StudentService
    ):
        """Test student ID generation"""
        student_id = await student_service.generate_student_id(db_session)

        assert student_id is not None
        assert student_id.startswith("STU")
        assert len(student_id) > 3

    @pytest.mark.asyncio
    async def test_create_duplicate_email(
        self, db_session: AsyncSession, student_service: StudentService, sample_student: Student
    ):
        """Test creating student with duplicate email"""
        student_data = {
            "first_name": "Duplicate",
            "last_name": "User",
            "email": "john.doe@example.com",  # Duplicate email
            "phone": "1111111111",
            "date_of_birth": date(2002, 1, 1),
            "gender": "male",
            "program": "MBA"
        }

        with pytest.raises(Exception):  # Should raise integrity error
            await student_service.create_student(db_session, student_data)
