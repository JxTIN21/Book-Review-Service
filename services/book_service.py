from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import json

from models import Book
from schemas import BookCreate, BookResponse
from services.cache_service import CacheService

class BookService:
    def __init__(self, db: Session, cache_service: CacheService):
        self.db = db
        self.cache = cache_service
    
    async def get_books(self, skip: int = 0, limit: int = 100) -> List[BookResponse]:
        """Get books with caching - cache first, then database"""
        cache_key = f"books:list:{skip}:{limit}"
        
        # Try cache first
        cached_books = await self.cache.get(cache_key)
        if cached_books:
            return [BookResponse(**book) for book in cached_books]
        
        # Cache miss - fetch from database
        books = self.db.query(Book).offset(skip).limit(limit).all()
        book_responses = [BookResponse.model_validate(book) for book in books]
        
        # Update cache (fire and forget)
        books_dict = [book.model_dump() for book in book_responses]
        await self.cache.set(cache_key, books_dict)
        
        return book_responses
    
    async def create_book(self, book_data: BookCreate) -> BookResponse:
        """Create a new book and invalidate cache"""
        # Check for duplicate ISBN if provided
        if book_data.isbn:
            existing = self.db.query(Book).filter(Book.isbn == book_data.isbn).first()
            if existing:
                raise ValueError(f"Book with ISBN {book_data.isbn} already exists")
        
        # Create book
        db_book = Book(**book_data.dict())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        
        # Invalidate books cache
        await self.cache.invalidate_pattern("books:list:*")
        
        return BookResponse.model_validate(db_book)
    
    async def get_book_by_id(self, book_id: int) -> Book:
        """Get book by ID with validation"""
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise ValueError(f"Book with id {book_id} not found")
        return book