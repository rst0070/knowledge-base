from knowledge_base.core.port.embedder import Embedder
from knowledge_base.core.port.llm import LLMPort
from knowledge_base.core.entity.graph import Vertex
from typing import List


class SearchExistingEdgeService:
    def __init__(
        self,
        llm: LLMPort,
        embedder: Embedder,
    ):
        self.llm = llm
        self.embedder = embedder

    async def execute(
        self,
        system_id: str,
        vertices: List[Vertex],
    ):
        """
        search edges connecting the given vertices.
        """
        pass
