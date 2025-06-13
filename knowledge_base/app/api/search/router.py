from .dto import (
    SearchRequest,
    SearchResponse,
)
from fastapi import APIRouter, Depends
from knowledge_base.di.container import Container
from dependency_injector.wiring import inject, Provide
from knowledge_base.core.usecase.search import SearchKnowledgeUsecase

router = APIRouter(
    prefix="/v1/search", responses={404: {"description": "Not found url"}}
)


@router.post("/", response_model=SearchResponse)
@inject
async def search(
    body: SearchRequest,
    usecase: SearchKnowledgeUsecase = Depends(Provide[Container.search_usecase]),
) -> SearchResponse:
    result = await usecase.execute(system_id=body.system_id, query=body.query)

    data = [
        f"{edge.source.data}:{edge.source.data_type} "
        f"-> {edge.data}:{edge.data_type} "
        f"-> {edge.target.data}:{edge.target.data_type}"
        for edge in result
    ]
    return SearchResponse(data=data)
