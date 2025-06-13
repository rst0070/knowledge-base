from knowledge_base.core.entity.knowledge import KnowledgeSource
from knowledge_base.core.service.extraction import (
    VertexExtractionService,
    EdgeExtractionService,
)
from knowledge_base.core.service.search import SearchEdgeService
from knowledge_base.core.service.deletion import DeleteOldEdgeService
from knowledge_base.core.service.addition import AddNewEdgeService
import logging


logger = logging.getLogger(__name__)


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
        logger.info(
            {
                "log_type": "add_usecase:execute",
                "log_data": knowledge_src,
            }
        )

        vertices = await self.vertex_extraction_service.execute(
            knowledge_src.system_id, knowledge_src.data
        )

        logger.info(
            {
                "log_type": "add_usecase:execute:vertices_extracted",
                "log_data": vertices,
            }
        )

        new_edges = await self.edge_extraction_service.execute(
            knowledge_src.system_id, knowledge_src.data, vertices
        )

        logger.info(
            {
                "log_type": "add_usecase:execute:new_edges_extracted",
                "log_data": new_edges,
            }
        )

        old_edges = await self.search_edge_service.execute(
            knowledge_src.system_id, vertices
        )

        logger.info(
            {
                "log_type": "add_usecase:execute:old_edges_searched",
                "log_data": old_edges,
            }
        )

        existing_edges = await self.delete_old_edge_service.execute(
            knowledge_src.system_id, new_edges, old_edges
        )

        logger.info(
            {
                "log_type": "add_usecase:execute:remaining_edges",
                "log_data": existing_edges,
            }
        )

        return await self.add_new_edge_service.execute(
            knowledge_src.system_id, existing_edges, new_edges
        )
