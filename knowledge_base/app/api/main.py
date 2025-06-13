# from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
from functools import partial
from dotenv import load_dotenv
from knowledge_base.di.config import BaseConfig
from knowledge_base.di.container import Container
from knowledge_base.app.api.health.router import health_router
from knowledge_base.app.api.experimental.router import router as experimental_router
from knowledge_base.app.api.search.router import router as search_router
from knowledge_base.app.api.add.router import router as add_router


async def lifespan(app: FastAPI):
    load_dotenv()
    config = BaseConfig()
    container = Container()
    container.config.from_pydantic(config)
    container.unwire()
    container.wire(
        modules=[
            "knowledge_base.app.api.experimental.router",
            "knowledge_base.app.api.search.router",
            "knowledge_base.app.api.add.router",
        ]
    )

    app.state.container = container
    app.include_router(experimental_router)
    app.include_router(search_router)
    app.include_router(health_router)
    app.include_router(add_router)

    yield

    await container.shutdown_resources()


def get_application():
    app = FastAPI(lifespan=partial(lifespan))

    return app


app = get_application()
