from dependency_injector import containers, providers
from knowledge_base.infra.neo4j import get_neo4j_driver
from knowledge_base.infra.litellm import get_litellm_router
from knowledge_base.infra.fastembed import get_fastembed_embedding_model
from knowledge_base.infra.kafka import get_kafka_producer, get_kafka_consumer
from knowledge_base.core.component.graph import Neo4jGraphRepository
from knowledge_base.core.component.llm import LiteLLM
from knowledge_base.core.component.embedder import FastEmbed
from knowledge_base.core.component.queue_producer import KafkaQueueProducer
from knowledge_base.core.component.queue_consumer import KafkaQueueConsumer
from knowledge_base.core.service.extraction import (
    VertexExtractionService,
    EdgeExtractionService,
)
from knowledge_base.core.service.deletion import DeleteOldEdgeService
from knowledge_base.core.service.addition import AddNewEdgeService
from knowledge_base.core.service.search import SearchEdgeService
from knowledge_base.core.usecase.add import AddKnowledgeUsecase
from knowledge_base.core.usecase.search import SearchKnowledgeUsecase


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Infra

    neo4j_driver = providers.Resource(
        get_neo4j_driver,
        uri=config.neo4j_uri,
        username=config.neo4j_username,
        password=config.neo4j_password,
    )

    litellm_router = providers.Resource(
        get_litellm_router,
        gemini_api_key=config.gemini_api_key,
        redis_host=config.redis_host,
        redis_port=config.redis_port,
    )

    fastembed_embedding_model = providers.Resource(
        get_fastembed_embedding_model,
        embedding_model=config.embedding_model,
    )

    kafka_producer = providers.Resource(
        get_kafka_producer,
        bootstrap_server=config.kafka_bootstrap_server,
    )

    kafka_consumer = providers.Resource(
        get_kafka_consumer,
        bootstrap_server=config.kafka_bootstrap_server,
        topic=config.kafka_topic,
    )

    # Components

    graph_repository = providers.Singleton(
        Neo4jGraphRepository,
        driver=neo4j_driver,
    )

    llm_port = providers.Singleton(
        LiteLLM,
        litellm_router=litellm_router,
        model_name=config.llm_model,
    )

    embedder = providers.Singleton(
        FastEmbed,
        embedding_model=fastembed_embedding_model,
    )

    queue_producer = providers.Singleton(
        KafkaQueueProducer,
        kafka_producer=kafka_producer,
        topic=config.kafka_topic,
        partition=config.kafka_partition,
    )

    queue_consumer = providers.Singleton(
        KafkaQueueConsumer,
        kafka_consumer=kafka_consumer,
        topic=config.kafka_topic,
        partition=config.kafka_partition,
    )

    # Services

    vertex_extraction_service = providers.Factory(
        VertexExtractionService,
        llm=llm_port,
        embedder=embedder,
    )

    edge_extraction_service = providers.Factory(
        EdgeExtractionService,
        llm=llm_port,
    )

    search_edge_service = providers.Factory(
        SearchEdgeService,
        llm=llm_port,
        graph_repository=graph_repository,
    )

    delete_old_edge_service = providers.Factory(
        DeleteOldEdgeService,
        llm=llm_port,
        graph_repository=graph_repository,
    )

    add_new_edge_service = providers.Factory(
        AddNewEdgeService,
        llm=llm_port,
        graph_repository=graph_repository,
    )

    # Usecases

    add_usecase = providers.Factory(
        AddKnowledgeUsecase,
        vertex_extraction_service=vertex_extraction_service,
        edge_extraction_service=edge_extraction_service,
        search_edge_service=search_edge_service,
        delete_old_edge_service=delete_old_edge_service,
        add_new_edge_service=add_new_edge_service,
    )

    search_usecase = providers.Factory(
        SearchKnowledgeUsecase,
        vertex_extraction_service=vertex_extraction_service,
        search_edge_service=search_edge_service,
    )
