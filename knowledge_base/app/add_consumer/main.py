import asyncio
from knowledge_base.di.container import Container
from knowledge_base.di.config import BaseConfig
from dotenv import load_dotenv
from dependency_injector.wiring import inject, Provide
from knowledge_base.core.port.queue_consumer import QueueConsumer
from knowledge_base.core.usecase.add import AddKnowledgeUsecase


@inject
async def application(
    queue_consumer: QueueConsumer = Provide[Container.queue_consumer],
    add_usecase: AddKnowledgeUsecase = Provide[Container.add_usecase],
):
    while True:
        print("Waiting for knowledge source")
        knowledge_source = await queue_consumer.consume()
        print(knowledge_source)
        await add_usecase.execute(knowledge_source)
        print("Knowledge source added")


async def main():
    load_dotenv()
    config = BaseConfig()
    container = Container()
    container.config.from_pydantic(config)
    container.unwire()
    container.wire(modules=[__name__])

    await application()


if __name__ == "__main__":
    asyncio.run(main())
