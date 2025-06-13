import asyncio
from knowledge_base.di.container import Container
from knowledge_base.di.config import BaseConfig
from dotenv import load_dotenv
from dependency_injector.wiring import inject, Provide
from knowledge_base.core.port.queue_consumer import QueueConsumer
from knowledge_base.core.usecase.add import AddKnowledgeUsecase
from knowledge_base.infra.logging import init_logging, shutdown_logging
import logging

logger = logging.getLogger(__name__)


@inject
async def application(
    queue_consumer: QueueConsumer = Provide[Container.queue_consumer],
    add_usecase: AddKnowledgeUsecase = Provide[Container.add_usecase],
):
    while True:
        logger.info(
            {
                "log_type": "application:waiting",
                "log_data": "Waiting for knowledge source",
            }
        )

        knowledge_source = await queue_consumer.consume()
        logger.info(
            {
                "log_type": "application:knowledge_source_received",
                "log_data": knowledge_source,
            }
        )

        result = await add_usecase.execute(knowledge_source)

        logger.info(
            {
                "log_type": "application:knowledge_source_added",
                "log_data": result,
            }
        )


async def main():
    init_logging()
    load_dotenv()
    config = BaseConfig()
    container = Container()
    container.config.from_pydantic(config)
    container.unwire()
    container.wire(modules=[__name__])

    await application()

    shutdown_logging()


if __name__ == "__main__":
    asyncio.run(main())
