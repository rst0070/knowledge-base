from knowledge_base.core.entity.knowledge import KnowledgeSource
from knowledge_base.core.service.extraction import (
    VertexExtractionService,
    EdgeExtractionService,
)
from knowledge_base.core.service.search import SearchEdgeService
from knowledge_base.core.service.deletion import DeleteOldEdgeService
from knowledge_base.core.service.addition import AddNewEdgeService


class AddKnowledgeUsecase:
    def __init__(
        self,
        # queue_consumer: QueueConsumer,
        vertex_extraction_service: VertexExtractionService,
        edge_extraction_service: EdgeExtractionService,
        search_edge_service: SearchEdgeService,
        delete_old_edge_service: DeleteOldEdgeService,
        add_new_edge_service: AddNewEdgeService,
    ):
        # self.queue_consumer = queue_consumer
        self.vertex_extraction_service = vertex_extraction_service
        self.edge_extraction_service = edge_extraction_service
        self.search_edge_service = search_edge_service
        self.delete_old_edge_service = delete_old_edge_service
        self.add_new_edge_service = add_new_edge_service

    async def execute(self, knowledge_src: KnowledgeSource):
        """
        1. Extract vertices from the knowledge source
        2. Extract edges from the knowledge source
        3. Search existing edges
        4. Delete old and not-useful edges
        5. Add new edges
        """
        # await self.queue_consumer.consume()

        vertices = await self.vertex_extraction_service.execute(
            knowledge_src.system_id, knowledge_src.data
        )

        new_edges = await self.edge_extraction_service.execute(
            knowledge_src.system_id, knowledge_src.data, vertices
        )

        old_edges = await self.search_edge_service.execute(
            knowledge_src.system_id, vertices
        )

        existing_edges = await self.delete_old_edge_service.execute(
            new_edges, old_edges
        )

        await self.add_new_edge_service.execute(existing_edges, new_edges)
