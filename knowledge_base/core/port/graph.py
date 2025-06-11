from knowledge_base.core.entity.graph import Vertex, Edge
from typing import List
from abc import ABC


class GraphRepository(ABC):
    async def find_edges_by_embedding(
        self,
        system_id: str,
        embedding: list[float],
    ) -> List[Edge]:
        """
        Find edges by the given embedding.
        The embedding will be matched with
        the embedding of the source and target vertices.
        """
        pass

    async def find_src_vertices_by_embedding(
        self,
        system_id: str,
        embedding: list[float],
    ) -> List[Vertex]:
        """
        Find source vertices by the given embedding.
        The embedding will be matched with the embedding of the source vertices.
        """
        pass

    async def find_dst_vertices_by_embedding(
        self,
        system_id: str,
        embedding: list[float],
    ) -> List[Vertex]:
        """
        Find destination vertices by the given embedding.
        The embedding will be matched with the embedding of the destination vertices.
        """
        pass

    async def save_edges(
        self,
        edges: List[Edge],
    ):
        """
        Save the given edges.
        It automatically handles vertices.
        - if the source or target vertex does not exist, it will be created.
        - if the source or target vertex already exists, it will be updated.
        """
        pass
