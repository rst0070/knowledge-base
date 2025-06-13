from knowledge_base.core.port.llm import LLMPort
from knowledge_base.core.port.graph import GraphRepository
from knowledge_base.core.entity.graph import Vertex, Edge
from typing import List
import asyncio


class SearchEdgeService:
    def __init__(
        self,
        llm: LLMPort,
        graph_repository: GraphRepository,
    ):
        self.llm = llm
        self.graph_repository = graph_repository

    async def _process_vertex(
        self,
        system_id: str,
        vertex: Vertex,
    ) -> List[Edge]:
        """
        Process a single vertex.
        """
        result = await self.graph_repository.find_edges_by_embedding(
            system_id, vertex.embedding
        )
        return result

    async def execute(
        self,
        system_id: str,
        vertices: List[Vertex],
    ) -> List[Edge]:
        """
        search edges connecting the given vertices.

        1. Search edges by the embeddings of the vertices
        2. Return the edges
        """
        tasks = [self._process_vertex(system_id, vertex) for vertex in vertices]
        result = await asyncio.gather(*tasks, return_exceptions=True)

        edges = []
        for task_result in result:
            if isinstance(task_result, Exception):
                continue
            edges.extend(task_result)

        return edges
