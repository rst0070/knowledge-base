from knowledge_base.core.port.embedder import Embedder
from knowledge_base.core.port.llm import LLMPort
from knowledge_base.core.entity.graph import Edge
from knowledge_base.core.port.graph import GraphRepository
from typing import List
import os
import json


class AddNewEdgeService:
    def __init__(
        self,
        llm: LLMPort,
        embedder: Embedder,
        graph_repository: GraphRepository,
    ):
        self.llm = llm
        self.embedder = embedder
        self.graph_repository = graph_repository

        with open(
            os.path.join(os.path.dirname(__file__), "addition_prompt.txt"), "r"
        ) as f:
            self.addition_prompt = f.read()

    async def execute(self, old_edges: List[Edge], new_edges: List[Edge]):
        """
        Add the new edges to the graph.
        return: List[Edge]
        """
        _old_edges = [
            {
                "id": i,
                "source": {
                    "data": edge.source.data,
                    "data_type": edge.source.data_type,
                },
                "target": {
                    "data": edge.target.data,
                    "data_type": edge.target.data_type,
                },
            }
            for i, edge in enumerate(old_edges)
        ]

        _new_edges = [
            {
                "id": i,
                "source": {
                    "data": edge.source.data,
                    "data_type": edge.source.data_type,
                },
                "target": {
                    "data": edge.target.data,
                    "data_type": edge.target.data_type,
                },
            }
            for i, edge in enumerate(new_edges)
        ]

        response = await self.llm.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": self.addition_prompt,
                },
                {
                    "role": "user",
                    "content": f"""
                    <old-edges>
                    {json.dumps(_old_edges)}
                    </old-edges>
                    <new-edges>
                    {json.dumps(_new_edges)}
                    </new-edges>
                    """,
                },
            ]
        )
        result = json.loads(response)
        added_ids = result["ids"]

        await self.graph_repository.save_edges([new_edges[i] for i in added_ids])

        return [new_edges[i] for i in added_ids]
