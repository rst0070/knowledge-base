from knowledge_base.app.api.dto.knowledge import (
    AddRequest,
    AddResponse,
    SearchResponse,
)
from fastapi import APIRouter
from knowledge_base.core.entity.knowledge import KnowledgeSource
from knowledge_base.app.api.service.knowledge import add_knowledge, search_knowledge

router = APIRouter(
    prefix="/v1/knowledge", responses={404: {"description": "Not found url"}}
)


@router.post("/", response_model=AddResponse)
async def add(
    body: AddRequest,
    # background_tasks: BackgroundTasks
) -> AddResponse:
    """
    Add knowledge to knowledge base
    This endpoint produces data to kafka queue
    """
    source_list = [
        KnowledgeSource(
            system_id=item.system_id,
            data=item.data,
            metadata=item.metadata,
        )
        for item in body.items
    ]

    await add_knowledge(source_list)

    return AddResponse(message="Success")


@router.get("/", response_model=SearchResponse)
async def search(
    system_id: str,
    query: str,
) -> SearchResponse:
    """
    Search knowledge from knowledge base
    """
    result = await search_knowledge(system_id=system_id, query=query)

    data = [
        f"{edge.source.data}:{edge.source.data_type} "
        f"-> {edge.data}:{edge.data_type} "
        f"-> {edge.target.data}:{edge.target.data_type}"
        for edge in result
    ]
    return SearchResponse(data=data)
