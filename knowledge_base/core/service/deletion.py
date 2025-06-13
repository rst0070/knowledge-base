from knowledge_base.core.port.llm import LLMPort
from knowledge_base.core.entity.graph import Edge
from typing import List
import json
import os
from knowledge_base.core.port.graph import GraphRepository


class DeleteOldEdgeService:
    def __init__(
        self,
        llm: LLMPort,
        graph_repository: GraphRepository,
    ):
        self.llm = llm
        self.graph_repository = graph_repository

        with open(
            os.path.realpath(
                os.path.join(
                    os.path.dirname(__file__), "../prompt", "old_edge_deletion.txt"
                )
            ),
            "r",
        ) as f:
            self.deletion_prompt = f.read()

    async def execute(
        self,
        system_id: str,
        new_edges: List[Edge],
        old_edges: List[Edge],
    ) -> List[Edge]:
        """
        Find what edges to delete, and delete them.

        return: not deleted edges among old_edges
        """

        _new_edges = [
            {
                "id": i,
                "source": {
                    "data": edge.source.data,
                    "data_type": edge.source.data_type,
                },
                "relationship": edge.data_type,
                "relationship_detail": edge.data,
                "target": {
                    "data": edge.target.data,
                    "data_type": edge.target.data_type,
                },
            }
            for i, edge in enumerate(new_edges)
        ]

        _old_edges = [
            {
                "id": i,
                "source": {
                    "data": edge.source.data,
                    "data_type": edge.source.data_type,
                },
                "relationship": edge.data_type,
                "relationship_detail": edge.data,
                "target": {
                    "data": edge.target.data,
                    "data_type": edge.target.data_type,
                },
            }
            for i, edge in enumerate(old_edges)
        ]

        response = await self.llm.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": self.deletion_prompt.replace("{{SYSTEM_ID}}", system_id),
                },
                {
                    "role": "user",
                    "content": f"""
                    <old-edges>
                    {json.dumps(_old_edges, ensure_ascii=False)}
                    </old_edges>
                    <new_edges>
                    {json.dumps(_new_edges, ensure_ascii=False)}
                    </new_edges>
                    """,
                },
            ],
            response_format={"type": "json_object"},
        )

        result = json.loads(response)
        deleted_ids = result["ids"]

        await self.graph_repository.delete_edges([old_edges[i] for i in deleted_ids])

        return [old_edges[i] for i in range(len(old_edges)) if i not in deleted_ids]
