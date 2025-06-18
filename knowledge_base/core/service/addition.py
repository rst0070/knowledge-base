from knowledge_base.core.port.llm import LLMPort
from knowledge_base.core.entity.graph import Edge
from knowledge_base.core.port.graph import GraphRepository
from jinja2 import Template
from typing import List
import os
import json


class AddNewEdgeService:
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
                    os.path.dirname(__file__), "../prompt", "new_edge_addtion.jinja2"
                )
            ),
            "r",
        ) as f:
            self.addition_prompt = Template(f.read())

    async def execute(
        self, system_id: str, old_edges: List[Edge], new_edges: List[Edge]
    ):
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
                "relationship": edge.data_type,
                "relationship_detail": edge.data,
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
                "relationship": edge.data_type,
                "relationship_detail": edge.data,
            }
            for i, edge in enumerate(new_edges)
        ]

        response = await self.llm.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": self.addition_prompt.render(
                        SYSTEM_ID=system_id,
                    ),
                },
                {
                    "role": "user",
                    "content": f"""
                    <old-edges>
                    {json.dumps(_old_edges, ensure_ascii=False)}
                    </old-edges>
                    <new-edges>
                    {json.dumps(_new_edges, ensure_ascii=False)}
                    </new-edges>
                    """,
                },
            ],
            response_format={"type": "json_object"},
        )
        result = json.loads(response)
        added_ids = result["ids"]

        await self.graph_repository.save_edges([new_edges[i] for i in added_ids])

        return [new_edges[i] for i in added_ids]
