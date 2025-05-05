from kafka import KafkaProducer, KafkaConsumer


def get_kafka_producer(bootstrap_servers: list[str]) -> KafkaProducer:
    return KafkaProducer(bootstrap_servers=bootstrap_servers)


def get_kafka_consumer(bootstrap_servers: list[str]) -> KafkaConsumer:
    return KafkaConsumer(bootstrap_servers=bootstrap_servers)
