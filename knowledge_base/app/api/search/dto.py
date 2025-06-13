from pydantic import BaseModel, Field
from typing import List


class SearchRequest(BaseModel):
    system_id: str = Field(..., description="System ID")
    query: str = Field(..., description="Query")
    limit: int = Field(..., description="Limit")


class SearchResponse(BaseModel):
    data: List[str]
