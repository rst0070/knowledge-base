from .dto import (
    AddRequest,
    AddResponse,
    SearchResponse,
)
from fastapi import APIRouter, Depends, BackgroundTasks
from knowledge_base.di.container import Container
from dependency_injector.wiring import inject, Provide
from knowledge_base.core.entity.knowledge import KnowledgeSource
from knowledge_base.core.port.queue_producer import QueueProducer
from knowledge_base.core.usecase.search import SearchKnowledgeUsecase
from typing import List
import asyncio

router = APIRouter(
    prefix="/v1/knowledge", responses={404: {"description": "Not found url"}}
)


async def add_producer(
    source_list: List[KnowledgeSource],
    queue_producer: QueueProducer,
):
    tasks = []
    for source in source_list:
        tasks.append(queue_producer.produce(source))

    await asyncio.gather(*tasks)

    return AddResponse(message="Success")


@router.post("/", response_model=AddResponse)
@inject
async def add(
    body: AddRequest,
    background_tasks: BackgroundTasks,
    queue_producer: QueueProducer = Depends(Provide[Container.queue_producer]),
) -> AddResponse:
    """
    Add knowledge to knowledge base
    This endpoint produces data to kafka queue
    """
    background_tasks.add_task(
        add_producer,
        [
            KnowledgeSource(
                system_id=item.system_id,
                data=item.data,
                metadata=item.metadata,
            )
            for item in body.items
        ],
        queue_producer=queue_producer,
    )

    return AddResponse(message="Success")


@router.get("/", response_model=SearchResponse)
@inject
async def search(
    system_id: str,
    query: str,
    usecase: SearchKnowledgeUsecase = Depends(Provide[Container.search_usecase]),
) -> SearchResponse:
    """
    Search knowledge from knowledge base
    """
    result = await usecase.execute(system_id=system_id, query=query)

    data = [
        f"{edge.source.data}:{edge.source.data_type} "
        f"-> {edge.data}:{edge.data_type} "
        f"-> {edge.target.data}:{edge.target.data_type}"
        for edge in result
    ]
    return SearchResponse(data=data)
