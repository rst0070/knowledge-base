from pydantic import BaseModel, Field
from typing import List, Optional


class AddRequestItem(BaseModel):
    system_id: str = Field(..., description="System ID")
    data: str = Field(..., description="Source of knowledge")
    metadata: Optional[dict] = Field(
        None, description="Metadata to be saved with knowledge"
    )


class AddRequest(BaseModel):
    items: List[AddRequestItem] = Field(..., description="Items to be added")


class AddResponse(BaseModel):
    message: str = Field(..., description="Message")


class SearchResponse(BaseModel):
    data: List[str]
