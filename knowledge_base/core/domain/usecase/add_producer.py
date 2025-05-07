from typing import Optional, List
from knowledge_base.core.domain.port.add_queue import AddQueue
from knowledge_base.core.domain.entity.knowledge import Knowledge
import asyncio


class AddProducerUsecase:
    def __init__(self, add_queue: AddQueue, max_concurrency: int = 10):
        self.add_queue = add_queue
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def execute(
        self, 
        batch: List[Knowledge]
    ):
        async with self.semaphore:
            async for knowledge in batch:
                await self.add_queue.put(knowledge)
