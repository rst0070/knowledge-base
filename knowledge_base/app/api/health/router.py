from fastapi import APIRouter, Response


health_router = APIRouter(
    prefix="",
    responses={404: {"description": "Not found url"}},
)


@health_router.get("/_health")
async def health():
    return Response(content="OK", media_type="text/plain")
