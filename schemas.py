from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, pattern=r'^\d{10}(\d{3})?$')
    description: Optional[str] = None
    published_year: Optional[int] = Field(None, ge=1000, le=2030)

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    reviewer_name: str = Field(..., min_length=1, max_length=255)
    rating: float = Field(..., ge=1.0, le=5.0)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    book_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True