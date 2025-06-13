from knowledge_base.core.service.extraction import VertexExtractionFromQueryService
from knowledge_base.core.service.search import SearchEdgeService
from knowledge_base.core.entity.graph import Edge
from typing import List


class SearchKnowledgeUsecase:
    def __init__(
        self,
        vertex_extraction_service: VertexExtractionFromQueryService,
        search_edge_service: SearchEdgeService,
    ):
        self.vertex_extraction_service = vertex_extraction_service
        self.search_edge_service = search_edge_service

    async def execute(self, system_id: str, query: str) -> List[Edge]:
        """
        1. Extract vertices from the query
        2. Search edges
        3. Return the edges
        """
        vertices = await self.vertex_extraction_service.execute(system_id, query)
        print(vertices)
        edges = await self.search_edge_service.execute(system_id, vertices)
        print(edges)
        return edges
