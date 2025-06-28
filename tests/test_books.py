import pytest
from fastapi.testclient import TestClient

def test_create_book(client: TestClient):
    """Test creating a new book"""
    book_data = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "9780743273565",
        "description": "A classic American novel",
        "published_year": 1925
    }
    
    response = client.post("/books", json=book_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]
    assert data["isbn"] == book_data["isbn"]
    assert "id" in data
    assert "created_at" in data

def test_create_book_duplicate_isbn(client: TestClient):
    """Test creating book with duplicate ISBN fails"""
    book_data = {
        "title": "Book 1",
        "author": "Author 1",
        "isbn": "1234567890123"
    }
    
    # Create first book
    response1 = client.post("/books", json=book_data)
    assert response1.status_code == 201
    
    # Try to create duplicate
    book_data["title"] = "Book 2"
    response2 = client.post("/books", json=book_data)
    assert response2.status_code == 400

def test_list_books_empty(client: TestClient):
    """Test listing books when none exist"""
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

def test_list_books_with_data(client: TestClient):
    """Test listing books with data"""
    # Create test books
    books = [
        {"title": "Book 1", "author": "Author 1"},
        {"title": "Book 2", "author": "Author 2"}
    ]
    
    created_books = []
    for book in books:
        response = client.post("/books", json=book)
        assert response.status_code == 201
        created_books.append(response.json())
    
    # List books
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_list_books_pagination(client: TestClient):
    """Test book pagination"""
    # Create multiple books
    for i in range(5):
        book_data = {"title": f"Book {i}", "author": f"Author {i}"}
        client.post("/books", json=book_data)
    
    # Test pagination
    response = client.get("/books?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2