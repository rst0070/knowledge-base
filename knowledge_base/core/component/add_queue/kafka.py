from knowledge_base.core.domain.port.add_queue import AddQueue
from kafka import KafkaProducer, KafkaConsumer
from knowledge_base.core.domain.entity.knowledge import Knowledge


class KafkaAddQueue(AddQueue):
    def __init__(self, producer: KafkaProducer, consumer: KafkaConsumer):
        self.producer = producer
        self.consumer = consumer

    async def put(self, knowledge: Knowledge):
        self.producer.send(self.topic, knowledge)

    async def get(self) -> Knowledge:
        return self.consumer.poll(timeout_ms=1000)
