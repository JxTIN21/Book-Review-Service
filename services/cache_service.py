import redis
import json
import logging
from typing import Optional, Any
import os

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.default_ttl = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes
        self._client = None
        self._is_available = True
    
    @property
    def client(self):
        """Lazy Redis client initialization"""
        if self._client is None:
            try:
                self._client = redis.from_url(self.redis_url, decode_responses=True)
                # Test connection
                self._client.ping()
                self._is_available = True
                logger.info("Redis connection established")
            except Exception as e:
                logger.warning(f"Redis connection failed: {str(e)}")
                self._is_available = False
                self._client = None
        return self._client
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache with error handling"""
        if not self._is_available:
            return None
            
        try:
            if self.client:
                value = self.client.get(key)
                if value:
                    return json.loads(value)
        except Exception as e:
            logger.warning(f"Cache get error for key {key}: {str(e)}")
            self._is_available = False
        return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with error handling"""
        if not self._is_available:
            return False
            
        try:
            if self.client:
                ttl = ttl or self.default_ttl
                result = self.client.setex(key, ttl, json.dumps(value, default=str))
                return result
        except Exception as e:
            logger.warning(f"Cache set error for key {key}: {str(e)}")
            self._is_available = False
        return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self._is_available:
            return False
            
        try:
            if self.client:
                return bool(self.client.delete(key))
        except Exception as e:
            logger.warning(f"Cache delete error for key {key}: {str(e)}")
        return False
    
    async def invalidate_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern"""
        if not self._is_available:
            return 0
            
        try:
            if self.client:
                keys = self.client.keys(pattern)
                if keys:
                    return self.client.delete(*keys)
        except Exception as e:
            logger.warning(f"Cache invalidate error for pattern {pattern}: {str(e)}")
        return 0