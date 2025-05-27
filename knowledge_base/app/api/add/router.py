from .dto import (
    AddRequest,
    AddResponse,
)
from fastapi import APIRouter, Depends
from knowledge_base.app.api.di.container import Container
from dependency_injector.wiring import inject, Provide
from knowledge_base.core.domain.entity.knowledge import Knowledge
from knowledge_base.core.domain.usecase.add_producer import AddProducerUsecase


add_router = APIRouter(
    prefix="/v1/add",
    responses={404: {"description": "Not found url"}}
)


@add_router.post("/", response_model=AddResponse)
@inject
async def add(
    body: AddRequest,
    usecase: AddProducerUsecase = Depends(Provide[Container.add_producer_usecase]),
) -> AddResponse:
    batch = []
    for item in body.items:
        batch.append(
            Knowledge(
                user_id=item.user_id,
                data=item.data,
                metadata=item.metadata,
            )
        )

    await usecase.execute(
        batch=batch
    )

    return AddResponse(message="Success")
