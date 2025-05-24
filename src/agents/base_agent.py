import time
from abc import ABC, abstractmethod
from typing import Dict, Any
from src.models.schemas import AgentResponse
from src.utils.logger import setup_logger

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = setup_logger(name)
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        start_time = time.time()
        try:
            result = await self._execute_logic(input_data)
            execution_time = time.time() - start_time
            return AgentResponse(
                agent_name=self.name,
                success=True,
                data=result,
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(f"Error in {self.name}: {str(e)}")
            return AgentResponse(
                agent_name=self.name,
                success=False,
                error_message=str(e),
                execution_time=execution_time
            )
    
    @abstractmethod
    async def _execute_logic(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    def validate_input(self, input_data: Dict[str, Any], required_fields: list) -> bool:
        for field in required_fields:
            if field not in input_data:
                raise ValueError(f"Missing required field: {field}")
        return True
