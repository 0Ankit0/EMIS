"""Contract tests for Library API endpoints"""
import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

from tests.conftest import test_user, test_superuser


@pytest.mark.asyncio
async def test_get_books_list(client: AsyncClient, test_superuser):
    """Test GET /api/library/books endpoint"""
    response = await client.get("/api/library/books")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) or isinstance(data, dict)


@pytest.mark.asyncio
async def test_add_book(client: AsyncClient, test_superuser):
    """Test POST /api/library/books endpoint"""
    book_data = {
        "isbn": "978-1-234567-89-0",
        "title": "Test Book",
        "author": "Test Author",
        "publisher": "Test Publisher",
        "category": "Fiction",
        "total_copies": 5
    }
    
    response = await client.post("/api/library/books", json=book_data)
    
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["isbn"] == "978-1-234567-89-0"
    assert data["title"] == "Test Book"


@pytest.mark.asyncio
async def test_get_book_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/library/books/{id} endpoint"""
    # First create a book
    book_data = {
        "isbn": "978-0-111111-11-1",
        "title": "Sample Book",
        "author": "Sample Author",
        "publisher": "Sample Publisher",
        "category": "Non-Fiction",
        "total_copies": 3
    }
    
    create_response = await client.post("/api/library/books", json=book_data)
    assert create_response.status_code in [200, 201]
    created_book = create_response.json()
    
    # Then retrieve it
    response = await client.get(f"/api/library/books/{created_book['id']}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_book["id"]
    assert data["title"] == "Sample Book"


@pytest.mark.asyncio
async def test_update_book(client: AsyncClient, test_superuser):
    """Test PUT /api/library/books/{id} endpoint"""
    # Create a book
    book_data = {
        "isbn": "978-0-222222-22-2",
        "title": "Update Test",
        "author": "Original Author",
        "publisher": "Test Publisher",
        "category": "Fiction",
        "total_copies": 2
    }
    
    create_response = await client.post("/api/library/books", json=book_data)
    created_book = create_response.json()
    
    # Update it
    update_data = {
        "author": "Updated Author",
        "total_copies": 5
    }
    
    response = await client.put(
        f"/api/library/books/{created_book['id']}", 
        json=update_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["author"] == "Updated Author"
    assert data["total_copies"] == 5


@pytest.mark.asyncio
async def test_delete_book(client: AsyncClient, test_superuser):
    """Test DELETE /api/library/books/{id} endpoint"""
    # Create a book
    book_data = {
        "isbn": "978-0-333333-33-3",
        "title": "Delete Test",
        "author": "Test Author",
        "publisher": "Test Publisher",
        "category": "Fiction",
        "total_copies": 1
    }
    
    create_response = await client.post("/api/library/books", json=book_data)
    created_book = create_response.json()
    
    # Delete it
    response = await client.delete(f"/api/library/books/{created_book['id']}")
    
    assert response.status_code in [200, 204]
    
    # Verify deletion
    get_response = await client.get(f"/api/library/books/{created_book['id']}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_issue_book(client: AsyncClient, test_superuser):
    """Test POST /api/library/issue endpoint"""
    # Create a book and member first
    book_data = {
        "isbn": "978-0-444444-44-4",
        "title": "Issue Test Book",
        "author": "Test Author",
        "publisher": "Test Publisher",
        "category": "Fiction",
        "total_copies": 3
    }
    
    book_response = await client.post("/api/library/books", json=book_data)
    book = book_response.json()
    
    # Issue the book
    issue_data = {
        "book_id": book["id"],
        "member_id": test_superuser.id,
        "due_date": (datetime.utcnow() + timedelta(days=14)).isoformat()
    }
    
    response = await client.post("/api/library/issue", json=issue_data)
    
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["book_id"] == book["id"]
    assert data["status"] == "issued"


@pytest.mark.asyncio
async def test_return_book(client: AsyncClient, test_superuser):
    """Test POST /api/library/return endpoint"""
    # Create and issue a book first
    book_data = {
        "isbn": "978-0-555555-55-5",
        "title": "Return Test Book",
        "author": "Test Author",
        "publisher": "Test Publisher",
        "category": "Fiction",
        "total_copies": 2
    }
    
    book_response = await client.post("/api/library/books", json=book_data)
    book = book_response.json()
    
    issue_data = {
        "book_id": book["id"],
        "member_id": test_superuser.id,
        "due_date": (datetime.utcnow() + timedelta(days=14)).isoformat()
    }
    
    issue_response = await client.post("/api/library/issue", json=issue_data)
    issue = issue_response.json()
    
    # Return the book
    response = await client.post(f"/api/library/return/{issue['id']}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "returned"
    assert data["return_date"] is not None


@pytest.mark.asyncio
async def test_search_books(client: AsyncClient, test_superuser):
    """Test GET /api/library/search endpoint"""
    # Create a book
    book_data = {
        "isbn": "978-0-666666-66-6",
        "title": "Python Programming",
        "author": "John Smith",
        "publisher": "Tech Books",
        "category": "Programming",
        "total_copies": 4
    }
    
    await client.post("/api/library/books", json=book_data)
    
    # Search for it
    response = await client.get("/api/library/search?q=Python")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(book["title"] == "Python Programming" for book in data)


@pytest.mark.asyncio
async def test_get_overdue_books(client: AsyncClient, test_superuser):
    """Test GET /api/library/overdue endpoint"""
    response = await client.get("/api/library/overdue")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_member_borrowed_books(client: AsyncClient, test_superuser):
    """Test GET /api/library/members/{id}/borrowed endpoint"""
    response = await client.get(f"/api/library/members/{test_superuser.id}/borrowed")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_invalid_book_data(client: AsyncClient, test_superuser):
    """Test POST /api/library/books with invalid data"""
    invalid_data = {
        "title": "Missing Required Fields"
        # Missing isbn, author, publisher, etc.
    }
    
    response = await client.post("/api/library/books", json=invalid_data)
    
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_issue_unavailable_book(client: AsyncClient, test_superuser):
    """Test issuing a book with no available copies"""
    # Create a book with 0 available copies
    book_data = {
        "isbn": "978-0-777777-77-7",
        "title": "Unavailable Book",
        "author": "Test Author",
        "publisher": "Test Publisher",
        "category": "Fiction",
        "total_copies": 0
    }
    
    book_response = await client.post("/api/library/books", json=book_data)
    book = book_response.json()
    
    # Try to issue it
    issue_data = {
        "book_id": book["id"],
        "member_id": test_superuser.id,
        "due_date": (datetime.utcnow() + timedelta(days=14)).isoformat()
    }
    
    response = await client.post("/api/library/issue", json=issue_data)
    
    assert response.status_code in [400, 409]  # Bad request or conflict
