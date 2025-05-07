from dependency_injector import containers, providers
from knowledge_base.core.domain.usecase.add_producer import AddProducerUsecase
from knowledge_base.core.component.add_queue.kafka import KafkaAddQueue


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    add_queue = providers.Singleton(
        KafkaAddQueue,
        producer=config.producer,
        consumer=config.consumer,
    )
    
    add_producer_usecase = providers.Factory(
        AddProducerUsecase,
        add_queue=add_queue,
        max_concurrency=config.max_concurrency,
    )

