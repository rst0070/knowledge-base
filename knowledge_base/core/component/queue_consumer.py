from knowledge_base.core.port.queue_consumer import QueueConsumer
from knowledge_base.core.entity.knowledge import KnowledgeSource
from aiokafka import AIOKafkaConsumer
import json


class KafkaQueueConsumer(QueueConsumer):
    def __init__(self, kafka_consumer: AIOKafkaConsumer):
        self.kafka_consumer = kafka_consumer

    async def consume(self) -> KnowledgeSource:
        record = await self.kafka_consumer.getone()
        source = json.loads(record.value)

        return KnowledgeSource(
            system_id=source["system_id"],
            data=source["data"],
            metadata=source["metadata"],
        )
