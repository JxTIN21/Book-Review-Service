import pytest
from unittest.mock import MagicMock, patch
from services.cache_service import CacheService

@pytest.mark.asyncio
async def test_cache_service_get_success():
    """Test successful cache get operation"""
    with patch('redis.from_url') as mock_redis_from_url:
        mock_client = MagicMock()
        mock_client.ping.return_value = True
        mock_client.get.return_value = '{"key": "value"}'
        mock_redis_from_url.return_value = mock_client
        
        cache_service = CacheService()
        result = await cache_service.get("test_key")
        
        assert result == {"key": "value"}
        mock_client.get.assert_called_once_with("test_key")

@pytest.mark.asyncio
async def test_cache_service_get_miss():
    """Test cache get with cache miss"""
    with patch('redis.from_url') as mock_redis_from_url:
        mock_client = MagicMock()
        mock_client.ping.return_value = True
        mock_client.get.return_value = None  # Cache miss
        mock_redis_from_url.return_value = mock_client
        
        cache_service = CacheService()
        result = await cache_service.get("test_key")
        
        assert result is None

@pytest.mark.asyncio
async def test_cache_service_set_success():
    """Test successful cache set operation"""
    with patch('redis.from_url') as mock_redis_from_url:
        mock_client = MagicMock()
        mock_client.ping.return_value = True
        mock_client.setex.return_value = True
        mock_redis_from_url.return_value = mock_client
        
        cache_service = CacheService()
        result = await cache_service.set("test_key", {"data": "value"}, 300)
        
        assert result is True
        mock_client.setex.assert_called_once()

@pytest.mark.asyncio
async def test_cache_service_connection_failure():
    """Test cache service handles connection failures gracefully"""
    with patch('redis.from_url') as mock_redis_from_url:
        mock_redis_from_url.side_effect = Exception("Connection failed")
        
        cache_service = CacheService()
        
        # Should handle gracefully and return None/False
        get_result = await cache_service.get("test_key")
        set_result = await cache_service.set("test_key", "value")
        
        assert get_result is None
        assert set_result is False

@pytest.mark.asyncio
async def test_cache_service_invalidate_pattern():
    """Test cache pattern invalidation"""
    with patch('redis.from_url') as mock_redis_from_url:
        mock_client = MagicMock()
        mock_client.ping.return_value = True
        mock_client.keys.return_value = ['books:list:0:100', 'books:list:100:100']
        mock_client.delete.return_value = 2
        mock_redis_from_url.return_value = mock_client
        
        cache_service = CacheService()
        result = await cache_service.invalidate_pattern("books:list:*")
        
        assert result == 2
        mock_client.keys.assert_called_once_with("books:list:*")