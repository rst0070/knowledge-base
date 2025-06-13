from .dto import (
    AddRequest,
    AddResponse,
)
from fastapi import APIRouter, Depends
from knowledge_base.di.container import Container
from dependency_injector.wiring import inject, Provide
from knowledge_base.core.usecase.add import AddKnowledgeUsecase
from knowledge_base.core.entity.knowledge import KnowledgeSource

router = APIRouter(
    prefix="/v1/experimental", responses={404: {"description": "Not found url"}}
)


@router.post("/", response_model=AddResponse)
@inject
async def add(
    body: AddRequest,
    usecase: AddKnowledgeUsecase = Depends(Provide[Container.add_usecase]),
) -> AddResponse:
    for item in body.items:
        await usecase.execute(
            KnowledgeSource(
                system_id=item.system_id,
                data=item.data,
                metadata=item.metadata,
            )
        )

    return AddResponse(message="Success")
