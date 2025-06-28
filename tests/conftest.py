import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import get_db, Base
from services.cache_service import CacheService

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Create test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def mock_cache_service():
    """Mock cache service for testing"""
    class MockCacheService:
        def __init__(self):
            self._store = {}
            self._is_available = True
        
        async def get(self, key):
            return self._store.get(key) if self._is_available else None
        
        async def set(self, key, value, ttl=None):
            if self._is_available:
                self._store[key] = value
                return True
            return False
        
        async def delete(self, key):
            return self._store.pop(key, None) is not None if self._is_available else False
        
        async def invalidate_pattern(self, pattern):
            if not self._is_available:
                return 0
            keys_to_delete = [k for k in self._store.keys() if pattern.replace('*', '') in k]
            for key in keys_to_delete:
                del self._store[key]
            return len(keys_to_delete)
        
        def set_unavailable(self):
            self._is_available = False
    
    return MockCacheService()