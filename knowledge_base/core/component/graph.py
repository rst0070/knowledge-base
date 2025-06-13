from knowledge_base.core.port.graph import GraphRepository
from typing import List
from knowledge_base.core.entity.graph import Edge, Vertex
from neo4j import AsyncGraphDatabase
import asyncio


class Neo4jGraphRepository(GraphRepository):
    def __init__(
        self,
        driver: AsyncGraphDatabase,
    ):
        self.driver = driver

    async def find_edges_by_embedding(
        self,
        system_id: str,
        embedding: list[float],
    ) -> List[Edge]:
        """
        Find edges by the given embedding.
        """

        cypher_query = """
        MATCH (n)
        WHERE
            n.embedding IS NOT NULL
            AND n.system_id = $system_id
        WITH
            n,
            round(
                2 * vector.similarity.cosine(n.embedding, $embedding) - 1,
                4
            ) AS similarity
        CALL (n) {
            MATCH (n)-[r]->(m)
            RETURN
                n.data AS src_data,
                labels(n) AS src_data_type,
                n.embedding AS src_embedding,

                type(r) AS edge_data_type,
                r.data AS edge_data,

                m.data AS dst_data,
                labels(m) AS dst_data_type,
                m.embedding AS dst_embedding
            UNION
            MATCH (m)-[r]->(n)
            RETURN
                m.data AS src_data,
                labels(m) AS src_data_type,
                m.embedding AS src_embedding,

                type(r) AS edge_data_type,
                r.data AS edge_data,

                n.data AS dst_data,
                labels(n) AS dst_data_type,
                n.embedding AS dst_embedding
        }
        WITH
            distinct src_data,
            src_data_type,
            src_embedding,
            edge_data,
            edge_data_type,
            dst_data,
            dst_data_type,
            dst_embedding,
            similarity
        RETURN
            src_data,
            src_data_type,
            src_embedding,
            edge_data,
            edge_data_type,
            dst_data,
            dst_data_type,
            dst_embedding,
            similarity
        ORDER BY
            similarity DESC
        LIMIT
            $limit
        """

        params = {
            "system_id": system_id,
            "embedding": embedding,
            "limit": 100,
        }

        records, summary, keys = await self.driver.execute_query(cypher_query, params)
        edges = []
        for record in records:
            edges.append(
                Edge(
                    source=Vertex(
                        system_id=system_id,
                        data=record["src_data"],
                        data_type=record["src_data_type"],
                        embedding=record["src_embedding"],
                        metadata={},
                    ),
                    target=Vertex(
                        system_id=system_id,
                        data=record["dst_data"],
                        data_type=record["dst_data_type"],
                        embedding=record["dst_embedding"],
                        metadata={},
                    ),
                    data=record["edge_data"],
                    data_type=record["edge_data_type"],
                    system_id=system_id,
                    metadata={},
                )
            )

        return edges

    async def find_src_vertices_by_embedding(
        self,
        system_id: str,
        embedding: list[float],
    ) -> List[Vertex]:
        pass

    async def find_dst_vertices_by_embedding(
        self,
        system_id: str,
        embedding: list[float],
    ) -> List[Vertex]:
        pass

    async def save_edges(self, edges: List[Edge]):
        for edge in edges:
            cypher_query = f"""
            MERGE (
                src:{edge.source.data_type}
                {{
                    system_id: $system_id,
                    data: $source_data,
                    embedding: $source_embedding
                }}
            )
            MERGE (
                dst:{edge.target.data_type}
                {{
                    system_id: $system_id,
                    data: $target_data,
                    embedding: $target_embedding
                }}
            )
            MERGE
                (src)
                -[:{edge.data_type} {{system_id: $system_id, data: $edge_data}}]
                ->(dst)
            """
            params = {
                "system_id": edge.source.system_id,
                "source_data": edge.source.data,
                "source_embedding": edge.source.embedding,
                "target_data": edge.target.data,
                "target_embedding": edge.target.embedding,
                "edge_data": edge.data,
            }
            await self.driver.execute_query(cypher_query, **params)

    async def delete_edges(self, edges: List[Edge]):
        # https://neo4j.com/docs/cypher-manual/current/clauses/delete/#delete-relationships-only
        print("delete edges: ", edges)
        tasks = []
        for edge in edges:
            cypher_query = """
            MATCH (src)-[r]->(dst)
            WHERE
                src.system_id = $system_id
                AND src.data = $source_data
                AND labels(src) = $source_type

                AND r.system_id = $system_id
                AND r.data = $edge_data
                AND type(r) = $edge_data_type

                AND dst.system_id = $system_id
                AND dst.data = $target_data
                AND labels(dst) = $target_type
            DELETE r
            """
            params = {
                "system_id": edge.system_id,
                "source_data": edge.source.data,
                "source_type": edge.source.data_type,
                "edge_data": edge.data,
                "edge_data_type": edge.data_type,
                "target_data": edge.target.data,
                "target_type": edge.target.data_type,
            }
            tasks.append(self.driver.execute_query(cypher_query, params))

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    # Temp test code
    async def main():
        driver = AsyncGraphDatabase.driver(
            "neo4j://localhost:7687", auth=("neo4j", "thisispasswd")
        )
        graph_repository = Neo4jGraphRepository(driver)

        await graph_repository.save_edges(
            [
                Edge(
                    source=Vertex(
                        data="source_data",
                        data_type="source_type",
                        system_id="1",
                        embedding=[1, 2, 3],
                        metadata={},
                    ),
                    target=Vertex(
                        data="target_data",
                        data_type="target_type",
                        system_id="1",
                        embedding=[1, 2, 3],
                        metadata={},
                    ),
                    data="edge_data",
                    system_id="1",
                    metadata={},
                )
            ]
        )

        result = await graph_repository.find_edges_by_embedding(
            system_id="1",
            embedding=[1, 2, 3],
        )
        print(result)

        await graph_repository.delete_edges(
            [
                Edge(
                    source=Vertex(
                        data="source_data",
                        data_type="source_type",
                        system_id="1",
                        embedding=[1, 2, 3],
                        metadata={},
                    ),
                    target=Vertex(
                        data="target_data",
                        data_type="target_type",
                        system_id="1",
                        embedding=[1, 2, 3],
                        metadata={},
                    ),
                    data="edge_data",
                    system_id="1",
                    metadata={},
                )
            ]
        )

        result = await graph_repository.find_edges_by_embedding(
            system_id="1",
            embedding=[1, 2, 3],
        )
        print(result)

    asyncio.run(main())
