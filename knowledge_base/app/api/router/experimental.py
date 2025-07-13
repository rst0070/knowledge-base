from knowledge_base.app.api.dto.knowledge import (
    AddRequest,
    AddResponse,
)
from fastapi import APIRouter
from knowledge_base.core.entity.knowledge import KnowledgeSource
from knowledge_base.app.api.service.knowledge import add_knowledge_exp

router = APIRouter(
    prefix="/v1/experimental", responses={404: {"description": "Not found url"}}
)


@router.post("/", response_model=AddResponse)
async def add(
    body: AddRequest,
) -> AddResponse:
    source_list = [
        KnowledgeSource(
            system_id=item.system_id,
            data=item.data,
            metadata=item.metadata,
        )
        for item in body.items
    ]
    await add_knowledge_exp(source_list)

    return AddResponse(message="Success")
