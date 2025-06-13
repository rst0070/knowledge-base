from knowledge_base.core.port.queue_consumer import QueueConsumer
from knowledge_base.core.entity.knowledge import KnowledgeSource
from aiokafka.structs import TopicPartition
from aiokafka import AIOKafkaConsumer
import json


class KafkaQueueConsumer(QueueConsumer):
    def __init__(self, kafka_consumer: AIOKafkaConsumer, topic: str, partition: int):
        self.kafka_consumer = kafka_consumer
        self.partition = TopicPartition(topic, partition)
        self._ready = False

    async def consume(self) -> KnowledgeSource:
        if not self._ready:
            print("Starting consumer")
            await self.kafka_consumer.start()

            print("Seeking to beginning")
            await self.kafka_consumer.seek_to_beginning(self.partition)
            self._ready = True
            print("Ready")

        record = await self.kafka_consumer.getone()

        source = json.loads(record.value)

        return KnowledgeSource(
            system_id=source["system_id"],
            data=source["data"],
            metadata=source["metadata"],
        )
