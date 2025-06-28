from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - defaults to SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./book_reviews.db")

# For PostgreSQL: "postgresql://user:password@localhost/book_reviews"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Databse dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()