from sqlalchemy.orm import Session
from typing import List

from models import Review, Book
from schemas import ReviewCreate, ReviewResponse
from services.cache_service import CacheService

class ReviewService:
    def __init__(self, db: Session, cache_service: CacheService):
        self.db = db
        self.cache = cache_service
    
    async def get_reviews_by_book(self, book_id: int, skip: int = 0, limit: int = 100) -> List[ReviewResponse]:
        """Get reviews for a book (optimized with index)"""
        # Verify book exists
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise ValueError(f"Book with id {book_id} not found")
        
        # Cache key for book reviews
        cache_key = f"reviews:book:{book_id}:{skip}:{limit}"
        
        # Try cache first
        cached_reviews = await self.cache.get(cache_key)
        if cached_reviews:
            return [ReviewResponse(**review) for review in cached_reviews]
        
        # Fetch from database using optimized query with index
        reviews = (
            self.db.query(Review)
            .filter(Review.book_id == book_id)
            .order_by(Review.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        review_responses = [ReviewResponse.model_validate(review) for review in reviews]
        
        # Cache results
        reviews_dict = [review.dict() for review in review_responses]
        await self.cache.set(cache_key, reviews_dict)
        
        return review_responses
    
    async def create_review(self, book_id: int, review_data: ReviewCreate) -> ReviewResponse:
        """Create a new review for a book"""
        # Verify book exists
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise ValueError(f"Book with id {book_id} not found")
        
        # Create review
        db_review = Review(book_id=book_id, **review_data.model_dump())
        self.db.add(db_review)
        self.db.commit()
        self.db.refresh(db_review)
        
        # Invalidate related caches
        await self.cache.invalidate_pattern(f"reviews:book:{book_id}:*")
        
        return ReviewResponse.model_validate(db_review)