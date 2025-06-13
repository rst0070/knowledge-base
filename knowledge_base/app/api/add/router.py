from .dto import (
    AddRequest,
    AddResponse,
)
from fastapi import APIRouter, Depends, BackgroundTasks
from knowledge_base.di.container import Container
from dependency_injector.wiring import inject, Provide
from knowledge_base.core.entity.knowledge import KnowledgeSource
from knowledge_base.core.port.queue_producer import QueueProducer
from typing import List
import asyncio

router = APIRouter(prefix="/v1/add", responses={404: {"description": "Not found url"}})


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
