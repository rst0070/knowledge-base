from dependency_injector import containers, providers
from knowledge_base.core.domain.usecase.add_producer import AddProducerUsecase
from knowledge_base.core.component.add_queue.kafka import KafkaAddQueue
from aiokafka import AIOKafkaProducer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    kafka_producer = providers.Singleton(
        AIOKafkaProducer,
        bootstrap_servers=config.kafka_bootstrap_servers,
    )

    add_queue = providers.Singleton(
        KafkaAddQueue,
        producer=kafka_producer,
        consumer=None,
    )
    
    add_producer_usecase = providers.Factory(
        AddProducerUsecase,
        add_queue=add_queue,
        max_concurrency=config.max_concurrency,
    )

