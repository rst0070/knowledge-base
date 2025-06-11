from knowledge_base.core.entity.knowledge import Knowledge
from knowledge_base.core.port.queue_consumer import QueueConsumer
from knowledge_base.core.service.extraction import (
    VertexExtractionService,
    EdgeExtractionService,
)
from knowledge_base.core.service.search import SearchExistingEdgeService


class AddKnowledgeUsecase:
    def __init__(
        self,
        queue_consumer: QueueConsumer,
        vertex_extraction_service: VertexExtractionService,
        edge_extraction_service: EdgeExtractionService,
        search_service: SearchExistingEdgeService,
    ):
        self.queue_consumer = queue_consumer
        self.vertex_extraction_service = vertex_extraction_service
        self.edge_extraction_service = edge_extraction_service

    async def execute(self, knowledge: Knowledge):
        """ """
        await self.queue_consumer.consume()

        vertices = await self.vertex_extraction_service.execute(
            knowledge.system_id, knowledge.text
        )
        await self.edge_extraction_service.execute(
            knowledge.system_id, knowledge.text, vertices
        )

        await self.search_service.execute(knowledge.system_id, vertices)

        # TODO:
        # 1. Resolve Conflict b/w Old and New Relationship
