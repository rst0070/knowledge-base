from abc import ABC, abstractmethod
from typing import List


class LLM(ABC):
    @abstractmethod
    def generate_response(self, messages: List[dict]) -> str:
        pass

    @abstractmethod
    async def close(self):
        pass
