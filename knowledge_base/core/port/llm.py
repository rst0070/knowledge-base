from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any


class LLMPort(ABC):
    @abstractmethod
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        response_format=None,
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
    ) -> Any:
        pass
