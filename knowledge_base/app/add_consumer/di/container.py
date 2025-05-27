from dependency_injector import containers, providers
from knowledge_base.infra.litellm import get_litellm_router
from knowledge_base.core.domain.port.llm import LLMPort
from knowledge_base.core.component.llm.litellm import LiteLLM


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # LLM Settings
    litellm_router = providers.Singleton(
        get_litellm_router,
        gemini_api_key=config.gemini_api_key,
    )

    llm_port: LLMPort = providers.Singleton(
        LiteLLM,
        litellm_router=litellm_router,
        model_name=config.llm_model_name,
    )

    # Kafka Settings
    kafka_producer = providers.Singleton(
        KafkaProducer,
        bootstrap_servers=config.kafka_bootstrap_servers,
    )
    
    kafka_consumer = providers.Singleton(
        KafkaConsumer,
        bootstrap_servers=config.kafka_bootstrap_servers,
    )
    
    
    
