#from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from functools import partial
from dotenv import load_dotenv
from knowledge_base.app.api.di.config import BaseConfig
from knowledge_base.app.api.di.container import Container
from knowledge_base.app.api.add.router import add_router
from knowledge_base.app.api.health.router import health_router


async def lifespan(app: FastAPI):
    load_dotenv()
    config = BaseConfig()
    container = Container()
    container.config.from_pydantic(config)
    container.unwire()
    container.wire(
        modules=[
            "knowledge_base.app.api.add.router",
        ]
    )

    app.state.container = container
    app.include_router(add_router)
    app.include_router(health_router)

    yield

    await container.shutdown_resources()


def get_application():
    app = FastAPI(lifespan=partial(lifespan))
    
    return app


app = get_application()

mcp = FastApiMCP(
    app
)

mcp.mount()

@app.get("/users/{user_id}", operation_id="get_user_info")
async def read_user(user_id: int):
    return {"user_id": user_id}
