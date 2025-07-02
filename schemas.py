from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime
from typing import Optional, List

# -------------------------------
# 📘 Book Schemas
# -------------------------------
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

        model_config = {
            "from_attributes": True
        }

# -------------------------------
# ✍️ Review Schemas
# -------------------------------
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

# -------------------------------
# 🔐 Auth Schemas
# -------------------------------
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_-]+$')

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

    @validator('username')
    def validate_username(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain alphanumeric characters, hyphens, and underscores')
        return v.lower()  # Convert to lowercase for consistency

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_active: bool = True

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None