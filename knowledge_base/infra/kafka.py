from aiokafka import AIOKafkaProducer, AIOKafkaConsumer


def get_kafka_producer(bootstrap_server: str) -> AIOKafkaProducer:
    # return AIOKafkaProducer(bootstrap_servers=bootstrap_servers[0])
    return AIOKafkaProducer(bootstrap_servers=bootstrap_server, enable_idempotence=True)


def get_kafka_consumer(bootstrap_server: str, topic: str) -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_server,
        auto_offset_reset="earliest",
        group_id="knowledge-base-add-consumer",
    )
