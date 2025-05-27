from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    max_concurrency: int = 10


class KafkaConfig(BaseConfig):
    bootstrap_servers: str
