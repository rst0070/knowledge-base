from abc import ABC, abstractmethod
from knowledge_base.core.entity.knowledge import KnowledgeSource


class QueueProducer(ABC):
    @abstractmethod
    async def produce(self, source: KnowledgeSource):
        pass
