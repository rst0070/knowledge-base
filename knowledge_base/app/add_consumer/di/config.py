from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    logging_level: str = "INFO"

    llm_model_name: str = "gemini-2.0-flash"

    # LiteLLM configs
    gemini_api_key: str
    
    # Kafka configs
    kafka_bootstrap_servers: list[str]
    kafka_topic: str


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"
