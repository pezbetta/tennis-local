from fastapi import APIRouter, status
from fastapi.responses import PlainTextResponse, Response

from src.api.v1 import health, player, league, match


home_router = APIRouter()


@home_router.get("/", response_description="Homepage", include_in_schema=False)
async def home() -> Response:
    return PlainTextResponse("127.0.0.1", status_code=status.HTTP_200_OK)


api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(player.router)
api_router.include_router(league.router)
api_router.include_router(match.router)
