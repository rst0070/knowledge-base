from knowledge_base.core.domain.port.add_queue import AddQueue
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from knowledge_base.core.domain.entity.knowledge import Knowledge
from typing import Optional


class KafkaAddQueue(AddQueue):
    def __init__(self, producer: AIOKafkaProducer, consumer: AIOKafkaConsumer):
        self.producer = producer
        self.consumer = consumer

    async def put(self, knowledge: Knowledge):
        await self.producer.send_and_wait(self.topic, knowledge)

    async def get(self) -> Knowledge:
        return await self.consumer.poll(timeout_ms=1000)
