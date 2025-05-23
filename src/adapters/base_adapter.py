import httpx
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from src.utils.logger import setup_logger

class BaseAdapter(ABC):
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.logger = setup_logger(self.__class__.__name__)
        self.client = httpx.AsyncClient(timeout=30.0)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        if params is None:
            params = {}
        
        params.update(self._get_auth_params())
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            self.logger.error(f"Request failed: {e}")
            raise
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            raise
    
    @abstractmethod
    def _get_auth_params(self) -> Dict[str, str]:
        """Return authentication parameters for API requests"""
        pass
    
    async def close(self):
        await self.client.aclose()
