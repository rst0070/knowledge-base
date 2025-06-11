from abc import ABC, abstractmethod
from knowledge_base.core.entity.knowledge import KnowledgeSource


class QueueConsumer(ABC):
    @abstractmethod
    async def consume(self) -> KnowledgeSource:
        pass
