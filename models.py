from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from sqlalchemy import text

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False)
    isbn = Column(String(13), unique=True, nullable=True)
    description = Column(Text, nullable=True)
    published_year = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reviewer_name = Column(String(255), nullable=False)
    rating = Column(Float, nullable=False)  # 1.0 to 5.0
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    book = relationship("Book", back_populates="reviews")
    
    # Index for optimized queries by book_id
    __table_args__ = (
        Index('idx_reviews_book_id', 'book_id'),
        Index('idx_reviews_book_rating', 'book_id', 'rating'),
    )