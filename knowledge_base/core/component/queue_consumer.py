from knowledge_base.core.port.queue_consumer import QueueConsumer
from knowledge_base.core.entity.knowledge import KnowledgeSource
from aiokafka.structs import TopicPartition
from aiokafka import AIOKafkaConsumer
import json
import logging

logger = logging.getLogger(__name__)


class KafkaQueueConsumer(QueueConsumer):
    def __init__(self, kafka_consumer: AIOKafkaConsumer, topic: str, partition: int):
        self.kafka_consumer = kafka_consumer
        self.partition = TopicPartition(topic, partition)
        self._ready = False

    async def consume(self) -> KnowledgeSource:
        if not self._ready:
            logger.info(
                {
                    "log_type": "queue_consumer:consume:starting_consumer",
                    "log_data": "Starting consumer",
                }
            )
            await self.kafka_consumer.start()

            logger.info(
                {
                    "log_type": "queue_consumer:consume:seeking_to_beginning",
                    "log_data": "Seeking to beginning",
                }
            )
            await self.kafka_consumer.seek_to_beginning(self.partition)
            self._ready = True
            logger.info(
                {
                    "log_type": "queue_consumer:consume:ready",
                    "log_data": "Ready",
                }
            )

        record = await self.kafka_consumer.getone()

        source = json.loads(record.value.decode("utf-8"))
        logger.info(
            {
                "log_type": "queue_consumer:consume:source_received",
                "log_data": source,
            }
        )

        return KnowledgeSource(
            system_id=source["system_id"],
            data=source["data"],
            metadata=source["metadata"],
        )
