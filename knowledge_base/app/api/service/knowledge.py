from knowledge_base.di.container import Container
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from knowledge_base.core.entity.knowledge import Edge, KnowledgeSource
from knowledge_base.core.port.queue_producer import QueueProducer
from knowledge_base.core.usecase.add import AddKnowledgeUsecase
from knowledge_base.core.usecase.search import SearchKnowledgeUsecase
from typing import List
import asyncio


@inject
async def add_knowledge(
    source_list: List[KnowledgeSource],
    queue_producer: QueueProducer = Depends(Provide[Container.queue_producer]),
) -> None:
    """
    Use queue to pass data to kafka
    """
    tasks = []
    for source in source_list:
        tasks.append(queue_producer.produce(source))

    await asyncio.gather(*tasks)


@inject
async def add_knowledge_exp(
    source_list: List[KnowledgeSource],
    usecase: AddKnowledgeUsecase = Depends(Provide[Container.add_usecase]),
) -> None:
    """
    Use usecase to add knowledge
    """
    for source in source_list:
        await usecase.execute(source)


@inject
async def search_knowledge(
    system_id: str,
    query: str,
    usecase: SearchKnowledgeUsecase = Depends(Provide[Container.search_usecase]),
) -> List[Edge]:
    """
    Search knowledge base
    """
    result = await usecase.execute(system_id, query)
    return result