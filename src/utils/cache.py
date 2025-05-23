import asyncio
import json
import hashlib
from typing import Any, Optional, Callable
from functools import wraps
from cachetools import TTLCache
import redis.asyncio as redis
from src.config import settings

class CacheManager:
    def __init__(self):
        self.local_cache = TTLCache(maxsize=1000, ttl=300)  # 5 min TTL
        self.redis_client = None
        if settings.redis_url:
            self.redis_client = redis.from_url(settings.redis_url)
    
    def _generate_key(self, func_name: str, *args, **kwargs) -> str:
        key_data = f"{func_name}:{str(args)}:{str(sorted(kwargs.items()))}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    async def get(self, key: str) -> Optional[Any]:
        # Try local cache first
        if key in self.local_cache:
            return self.local_cache[key]
        
        # Try Redis if available
        if self.redis_client:
            try:
                data = await self.redis_client.get(key)
                if data:
                    result = json.loads(data)
                    self.local_cache[key] = result
                    return result
            except Exception:
                pass
        
        return None
    
    async def set(self, key: str, value: Any, ttl: int = 300):
        # Set in local cache
        self.local_cache[key] = value
        
        # Set in Redis if available
        if self.redis_client:
            try:
                await self.redis_client.setex(key, ttl, json.dumps(value, default=str))
            except Exception:
                pass

cache_manager = CacheManager()

def cached(ttl: int = 300):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = cache_manager._generate_key(func.__name__, *args, **kwargs)
            result = await cache_manager.get(key)
            
            if result is not None:
                return result
            
            result = await func(*args, **kwargs)
            await cache_manager.set(key, result, ttl)
            return result
        
        return wrapper
    return decorator
