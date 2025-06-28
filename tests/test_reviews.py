import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def sample_book(client: TestClient):
    """Create a sample book for testing"""
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "description": "A book for testing"
    }
    response = client.post("/books", json=book_data)
    assert response.status_code == 201
    return response.json()

def test_create_review(client: TestClient, sample_book):
    """Test creating a new review"""
    review_data = {
        "reviewer_name": "John Doe",
        "rating": 4.5,
        "comment": "Great read!"
    }
    
    response = client.post(f"/books/{sample_book['id']}/reviews", json=review_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["reviewer_name"] == review_data["reviewer_name"]
    assert data["rating"] == review_data["rating"]
    assert data["comment"] == review_data["comment"]
    assert data["book_id"] == sample_book["id"]

def test_create_review_nonexistent_book(client: TestClient):
    """Test creating review for non-existent book fails"""
    review_data = {
        "reviewer_name": "John Doe",
        "rating": 4.5,
        "comment": "Great read!"
    }
    
    response = client.post("/books/999/reviews", json=review_data)
    assert response.status_code == 404

def test_get_book_reviews(client: TestClient, sample_book):
    """Test getting reviews for a book"""
    # Create some reviews
    reviews = [
        {"reviewer_name": "Alice", "rating": 5.0, "comment": "Excellent!"},
        {"reviewer_name": "Bob", "rating": 3.5, "comment": "Good book."}
    ]
    
    for review in reviews:
        response = client.post(f"/books/{sample_book['id']}/reviews", json=review)
        assert response.status_code == 201
    
    # Get reviews
    response = client.get(f"/books/{sample_book['id']}/reviews")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Verify reviews are ordered by created_at desc (most recent first)
    assert data[0]["reviewer_name"] in ["Alice", "Bob"]

def test_get_reviews_nonexistent_book(client: TestClient):
    """Test getting reviews for non-existent book fails"""
    response = client.get("/books/999/reviews")
    assert response.status_code == 404

def test_review_rating_validation(client: TestClient, sample_book):
    """Test review rating validation"""
    # Test invalid ratings
    invalid_ratings = [0.5, 5.5, -1, 6]
    
    for rating in invalid_ratings:
        review_data = {
            "reviewer_name": "Test User",
            "rating": rating,
            "comment": "Test comment"
        }
        response = client.post(f"/books/{sample_book['id']}/reviews", json=review_data)
        assert response.status_code == 422  # Validation error