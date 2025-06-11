from knowledge_base.core.port.llm import LLMPort
from knowledge_base.core.port.embedder import Embedder
from knowledge_base.core.entity.graph import Vertex, Edge
from typing import List
import json
import os


class VertexExtractionService:
    def __init__(
        self,
        llm: LLMPort,
        embedder: Embedder,
    ):
        self.llm = llm
        self.embedder = embedder

        self.vertex_extraction_prompt = ""
        with open(
            os.path.join(
                os.path.dirname(__file__), "../prompt", "vertex_extraction.txt"
            ),
            "r",
        ) as f:
            self.vertex_extraction_prompt = f.read()

    async def execute(self, system_id: str, text: str) -> List[Vertex]:
        """
        Extract vertices(entities) from the given text.
        """
        result = await self.llm.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": self.vertex_extraction_prompt,
                },
                {
                    "role": "user",
                    "content": text,
                },
            ]
        )
        result = json.loads(result)

        vertices = []
        for vertex in result:
            vertices.append(
                Vertex(
                    system_id=system_id,
                    data=vertex["data"],
                    data_type=vertex["data_type"],
                )
            )
        return vertices


class EdgeExtractionService:
    def __init__(
        self,
        llm: LLMPort,
        embedder: Embedder,
    ):
        self.llm = llm
        self.embedder = embedder
        self.edge_extraction_prompt = ""
        with open(
            os.path.join(os.path.dirname(__file__), "../prompt", "edge_extraction.txt"),
            "r",
        ) as f:
            self.edge_extraction_prompt = f.read()

    async def execute(
        self, system_id: str, text: str, vertices: List[Vertex]
    ) -> List[Edge]:
        """
        Extract edges(relationships) between the given vertices from the given text.
        """
        vertices_json = [vertex.model_dump() for vertex in vertices]
        result = await self.llm.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": self.edge_extraction_prompt,
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "text-source": text,
                            "vertices": vertices_json,
                        }
                    ),
                },
            ]
        )
        result = json.loads(result)
        edges = []
        for edge in result:

            source = next(
                (vertex for vertex in vertices if vertex.data == edge["source"]), None
            )
            if source is None:
                continue

            target = next(
                (vertex for vertex in vertices if vertex.data == edge["target"]), None
            )
            if target is None:
                continue

            edges.append(
                Edge(
                    system_id=system_id,
                    data=edge["relationship"],
                    source=source,
                    target=target,
                )
            )
        return edges
