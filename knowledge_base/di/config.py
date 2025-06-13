from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):

    # Neo4j
    neo4j_uri: str = "neo4j://localhost:7687"
    neo4j_username: str = "neo4j"
    neo4j_password: str = "thisispasswd"

    # Litellm
    gemini_api_key: str

    # LLM
    llm_model: str = "gemini-2.0-flash"

    # Embedding
    embedding_model: str = "BAAI/bge-small-en-v1.5"
