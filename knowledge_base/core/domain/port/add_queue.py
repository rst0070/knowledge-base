from abc import ABC, abstractmethod
from typing import Optional
from knowledge_base.core.domain.entity.knowledge import Knowledge


class AddQueue(ABC):
    @abstractmethod
    async def put(self, knowledge: Knowledge):
        pass
    
    @abstractmethod
    async def get(self) -> Knowledge:
        pass

    @abstractmethod
    def close(self):
        pass
