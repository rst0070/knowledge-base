from knowledge_base.core.port.llm import LLMPort
from knowledge_base.core.port.embedder import Embedder
from knowledge_base.core.entity.graph import Vertex, Edge
from typing import List, Optional, Dict
from dataclasses import asdict
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
            os.path.realpath(
                os.path.join(
                    os.path.dirname(__file__), "../prompt", "vertex_extraction.txt"
                )
            ),
            "r",
        ) as f:
            self.vertex_extraction_prompt = f.read()

    async def execute(
        self, system_id: str, text: str, metadata: Optional[Dict] = None
    ) -> List[Vertex]:
        """
        Extract vertices(entities) from the given text.
        """
        result = await self.llm.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": self.vertex_extraction_prompt.replace(
                        "{{SYSTEM_ID}}", system_id
                    ),
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
            response_format={"type": "json_object"},
        )
        result = json.loads(result)

        vertices = []
        for vertex in result:
            vertices.append(
                Vertex(
                    system_id=system_id,
                    data=vertex["data"],
                    data_type=vertex["data_type"].replace(" ", "_"),
                    embedding=self.embedder.embed(vertex["data"]),
                    metadata=metadata or {},
                )
            )
        return vertices


class VertexExtractionFromQueryService:
    def __init__(self, llm: LLMPort, embedder: Embedder):
        self.llm = llm
        self.embedder = embedder

        self.vertex_extraction_from_query_prompt = ""
        with open(
            os.path.realpath(
                os.path.join(
                    os.path.dirname(__file__),
                    "../prompt",
                    "vertex_extraction_from_query.txt",
                )
            ),
            "r",
        ) as f:
            self.vertex_extraction_from_query_prompt = f.read()

    async def execute(
        self, system_id: str, query: str, metadata: Optional[Dict] = None
    ) -> List[Vertex]:
        """
        Extract vertices(entities) from the given query.
        """
        result = await self.llm.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": self.vertex_extraction_from_query_prompt.replace(
                        "{{SYSTEM_ID}}", system_id
                    ),
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
            response_format={"type": "json_object"},
        )
        result = json.loads(result)

        vertices = []
        for vertex in result:
            vertices.append(
                Vertex(
                    system_id=system_id,
                    data=vertex["data"],
                    data_type=vertex["data_type"].replace(" ", "_").replace("'", "_"),
                    embedding=self.embedder.embed(vertex["data"]),
                    metadata=metadata or {},
                )
            )
        return vertices


class EdgeExtractionService:
    def __init__(
        self,
        llm: LLMPort,
    ):
        self.llm = llm
        self.edge_extraction_prompt = ""
        with open(
            os.path.realpath(
                os.path.join(
                    os.path.dirname(__file__), "../prompt", "edge_extraction.txt"
                )
            ),
            "r",
        ) as f:
            self.edge_extraction_prompt = f.read()

    async def execute(
        self,
        system_id: str,
        text: str,
        vertices: List[Vertex],
        metadata: Optional[Dict] = None,
    ) -> List[Edge]:
        """
        Extract edges(relationships) between the given vertices from the given text.
        """
        vertices_json = [asdict(vertex) for vertex in vertices]
        result = await self.llm.generate_response(
            messages=[
                {
                    "role": "system",
                    "content": self.edge_extraction_prompt.replace(
                        "{{SYSTEM_ID}}", system_id
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "text-source": text,
                            "vertices": vertices_json,
                        },
                        ensure_ascii=False,
                    ),
                },
            ],
            response_format={"type": "json_object"},
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
                    data_type=edge["relationship"].replace(" ", "_").replace("'", "_"),
                    data=edge["relationship_detail"],
                    source=source,
                    target=target,
                    metadata=metadata or {},
                )
            )
        return edges
