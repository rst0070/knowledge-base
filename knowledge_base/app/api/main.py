# from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
from functools import partial
from dotenv import load_dotenv
from knowledge_base.di.config import BaseConfig
from knowledge_base.di.container import Container
from knowledge_base.app.api.router.health import health_router
from knowledge_base.app.api.router.experimental import router as experimental_router
from knowledge_base.app.api.router.knowledge import router as knowledge_router
from knowledge_base.app.api.router.mcp import router as mcp_router
from knowledge_base.infra.logging import init_logging, shutdown_logging


async def lifespan(app: FastAPI):
    init_logging()
    load_dotenv()
    config = BaseConfig()
    container = Container()
    container.config.from_pydantic(config)
    container.unwire()
    container.wire(
        modules=[
            "knowledge_base.app.api.service.knowledge",
        ]
    )

    app.state.container = container
    app.include_router(experimental_router)
    app.include_router(health_router)
    app.include_router(knowledge_router)
    app.include_router(mcp_router)

    yield

    await container.shutdown_resources()
    shutdown_logging()


def get_application():
    app = FastAPI(lifespan=partial(lifespan))

    return app


app = get_application()
