from knowledge_base.core.port.queue_producer import QueueProducer
from knowledge_base.core.entity.knowledge import KnowledgeSource
from aiokafka import AIOKafkaProducer
from dataclasses import asdict
import json


class KafkaQueueProducer(QueueProducer):
    def __init__(self, kafka_producer: AIOKafkaProducer, topic: str, partition: int):
        self.kafka_producer = kafka_producer
        self.topic = topic
        self.partition = partition

    async def produce(self, source: KnowledgeSource):
        try:
            await self.kafka_producer.start()
        except Exception as e:
            print(e)

        source_json = json.dumps(asdict(source), ensure_ascii=False)

        await self.kafka_producer.send_and_wait(
            self.topic, source_json.encode("utf-8"), partition=self.partition
        )
