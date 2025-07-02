from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
from schemas import Token, UserCreate, UserLogin
from database import get_db
from models import User
import os
from dotenv import load_dotenv

# -------------------------------
# 🔐 JWT Configuration
# -------------------------------
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-dev-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# -------------------------------
# 🔒 Password Hashing Context
# -------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------------------
# 🚪 Router Instance
# -------------------------------
auth_router = APIRouter(tags=["auth"])

# -------------------------------
# 📋 Response Models
# -------------------------------
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

# -------------------------------
# 🔐 Utility Functions
# -------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# -------------------------------
# 👤 Register Route
# -------------------------------
@auth_router.post("/signup", response_model=LoginResponse)
def register_user(request: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(request.password)
    new_user = User(email=request.email,  username=request.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.email})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "username": new_user.username  # Extract username from email
        }
    }

# -------------------------------
# 🔐 Login Route
# -------------------------------
@auth_router.post("/login", response_model=LoginResponse)
def login_user(request: UserLogin, db: Session = Depends(get_db)): 
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username  # Extract username from email
        }
    }