from aiokafka import AIOKafkaProducer, AIOKafkaConsumer


def get_kafka_producer(bootstrap_servers: list[str]) -> AIOKafkaProducer:
    # return AIOKafkaProducer(bootstrap_servers=bootstrap_servers[0])
    return AIOKafkaProducer(
        bootstrap_servers="localhost:29092", enable_idempotence=True
    )


def get_kafka_consumer(bootstrap_servers: list[str], topic: str) -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers[0],
        auto_offset_reset="earliest",
        group_id="knowledge-base-add-consumer",
    )
