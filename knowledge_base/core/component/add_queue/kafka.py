from knowledge_base.core.domain.port.add_queue import AddQueue
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from knowledge_base.core.domain.entity.knowledge import Knowledge
from typing import Optional


class KafkaAddQueue(AddQueue):
    def __init__(self, producer: Optional[AIOKafkaProducer], consumer: Optional[AIOKafkaConsumer]):
        self.producer = producer
        self.consumer = consumer

    async def put(self, knowledge: Knowledge):
        if self.producer is None:
            raise ValueError("Producer is not initialized")
        await self.producer.send_and_wait(self.topic, knowledge)

    async def get(self) -> Knowledge:
        if self.consumer is None:
            raise ValueError("Consumer is not initialized")
        return await self.consumer.poll(timeout_ms=1000)
