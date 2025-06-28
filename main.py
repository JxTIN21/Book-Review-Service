from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from contextlib import asynccontextmanager

from database import get_db, engine, Base
from models import Book, Review
from schemas import BookCreate, BookResponse, ReviewCreate, ReviewResponse
from services.book_service import BookService
from services.review_service import ReviewService
from services.cache_service import CacheService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting up Book Review Service")
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    logger.info("Shutting down Book Review Service")

app = FastAPI(
    title="Book Review Service",
    description="a RESTful API for managing books and their reviews",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencies
def get_book_service(db: Session = Depends(get_db)) -> BookService:
    cache_service = CacheService()
    return BookService(db, cache_service)

def get_review_service(db: Session = Depends(get_db)) -> ReviewService:
    cache_service = CacheService()
    return ReviewService(db, cache_service)

# Routes
@app.get("/books", response_model=List[BookResponse], tags=["Books"])
async def list_books(
    skip: int = 0,
    limit: int = 100,
    book_service: BookService = Depends(get_book_service)
):
    """
    Retrieve all books with caching support.
    
    First attempts to read from Redis cache, falls back to databse if cache miss or error.
    """
    try:
        books = await book_service.get_books(skip=skip, limit=limit)
        return books
    except Exception as e:
        logger.error(f"Error fetching books: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve books"
        )
    
@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED, tags=["books"])
async def create_book(
    book: BookCreate,
    book_service: BookService = Depends(get_book_service)
):
    """Create a new book"""
    try:
        new_book = await book_service.create_book(book)
        return new_book
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create book"
        )
    
@ app.get("/books/{book_id}/reviews", response_model=List[ReviewResponse], tags=["reviews"])
async def get_book_reviews(
    book_id: int,
    skip: int = 0,
    limit: int = 100,
    review_service: ReviewService = Depends(get_review_service)
):
    """Get a;; reviews for a specific book (optimized with index)"""
    try:
        reviews = await review_service.get_reviews_by_book(book_id, skip=skip, limit=limit)
        return reviews
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error fetching reviews for book {book_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve reviews"
        )
    
@app.post("/books/{book_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED, tags=["reviews"])
async def create_review(
    book_id: int,
    review: ReviewCreate,
    review_service: ReviewService = Depends(get_review_service)
):
    """Create a new review for a book"""
    try:
        new_review = await review_service.create_review(book_id, review)
        return new_review
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating review for book {book_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create review"
        )
    
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "book-review-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)