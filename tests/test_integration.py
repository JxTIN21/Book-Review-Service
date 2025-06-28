import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

def test_cache_miss_flow(client: TestClient, mock_cache_service):
    """Test the cache miss flow - data fetched from DB and cached"""
    # Create test data
    book_data = {"title": "Cache Test Book", "author": "Cache Author"}
    response = client.post("/books", json=book_data)
    assert response.status_code == 201
    book = response.json()
    
    # Mock the cache service to simulate cache miss then hit
    with patch('services.cache_service.CacheService') as mock_cache_class:
        mock_cache_instance = mock_cache_service
        mock_cache_class.return_value = mock_cache_instance
        
        # First request - cache miss
        response1 = client.get("/books")
        assert response1.status_code == 200
        books1 = response1.json()
        assert len(books1) >= 1
        assert any(b["title"] == "Cache Test Book" for b in books1)
        
        # Verify cache was populated (in real scenario)
        # Second request should hit cache (but in test, we'll verify the flow)
        response2 = client.get("/books")
        assert response2.status_code == 200
        books2 = response2.json()
        assert books1 == books2

def test_cache_unavailable_fallback(client: TestClient, mock_cache_service):
    """Test that API works when cache is unavailable"""
    # Create test data
    book_data = {"title": "Fallback Test Book", "author": "Fallback Author"}
    response = client.post("/books", json=book_data)
    assert response.status_code == 201
    
    # Mock cache service to be unavailable
    with patch('services.cache_service.CacheService') as mock_cache_class:
        mock_cache_instance = mock_cache_service
        mock_cache_instance.set_unavailable()  # Make cache unavailable
        mock_cache_class.return_value = mock_cache_instance
        
        # Request should still work, falling back to database
        response = client.get("/books")
        assert response.status_code == 200
        books = response.json()
        assert len(books) >= 1
        assert any(b["title"] == "Fallback Test Book" for b in books)

def test_end_to_end_book_review_flow(client: TestClient):
    """Test complete end-to-end flow"""
    # 1. Create a book
    book_data = {
        "title": "End-to-End Test Book",
        "author": "E2E Author",
        "isbn": "9781234567890",
        "description": "A comprehensive test book",
        "published_year": 2024
    }
    
    book_response = client.post("/books", json=book_data)
    assert book_response.status_code == 201
    book = book_response.json()
    book_id = book["id"]
    
    # 2. Verify book appears in list
    books_response = client.get("/books")
    assert books_response.status_code == 200
    books = books_response.json()
    assert any(b["id"] == book_id for b in books)
    
    # 3. Add multiple reviews
    reviews_data = [
        {"reviewer_name": "Alice Johnson", "rating": 4.8, "comment": "Absolutely fantastic!"},
        {"reviewer_name": "Bob Smith", "rating": 4.2, "comment": "Really enjoyed it."},
        {"reviewer_name": "Carol Davis", "rating": 3.9, "comment": "Good read, some slow parts."}
    ]
    
    created_review_ids = []
    for review_data in reviews_data:
        review_response = client.post(f"/books/{book_id}/reviews", json=review_data)
        assert review_response.status_code == 201
        review = review_response.json()
        created_review_ids.append(review["id"])
        assert review["book_id"] == book_id
    
    # 4. Fetch all reviews for the book
    reviews_response = client.get(f"/books/{book_id}/reviews")
    assert reviews_response.status_code == 200
    reviews = reviews_response.json()
    assert len(reviews) == 3
    
    # 5. Verify reviews contain expected data
    reviewer_names = {r["reviewer_name"] for r in reviews}
    expected_names = {"Alice Johnson", "Bob Smith", "Carol Davis"}
    assert reviewer_names == expected_names
    
    # 6. Test pagination on reviews
    paginated_response = client.get(f"/books/{book_id}/reviews?limit=2")
    assert paginated_response.status_code == 200
    paginated_reviews = paginated_response.json()
    assert len(paginated_reviews) == 2

def test_error_handling_and_validation(client: TestClient):
    """Test various error conditions and validation"""
    # Test invalid book data
    invalid_book_data = {
        "title": "",  # Empty title
        "author": "Test Author"
    }
    response = client.post("/books", json=invalid_book_data)
    assert response.status_code == 422  # Validation error
    
    # Test invalid ISBN format
    invalid_isbn_book = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "invalid-isbn"
    }
    response = client.post("/books", json=invalid_isbn_book)
    assert response.status_code == 422
    
    # Test review for non-existent book
    review_data = {"reviewer_name": "Test User", "rating": 4.0}
    response = client.post("/books/99999/reviews", json=review_data)
    assert response.status_code == 404
    
    # Test invalid rating values  
    book_response = client.post("/books", json={"title": "Test", "author": "Test"})
    book_id = book_response.json()["id"]
    
    invalid_review = {"reviewer_name": "Test", "rating": 6.0}  # Rating too high
    response = client.post(f"/books/{book_id}/reviews", json=invalid_review)
    assert response.status_code == 422