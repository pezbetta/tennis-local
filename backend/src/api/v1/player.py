from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.schemas.player import IPlayerUpdate
from src.db.session import get_session
from src.repositories.player import PlayerRepository
from src.core.enums import SortOrder
from src.schemas.common import IGetResponseBase
from src.schemas.player import IPlayerRead, IPlayerCreate

import logging
FORMAT = "%(levelname)s:%(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

logging.debug('This message should appear on the console')


router = APIRouter()


@router.get(
    "/player",
    response_description="List all players",
    response_model=IGetResponseBase[List[IPlayerRead]],
    tags=["players"],
)
async def list_all_players(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1),
    sort_field: Optional[str] = "id",
    sort_order: Optional[str] = SortOrder.DESC,
    session: AsyncSession = Depends(get_session),
) -> IGetResponseBase[List[IPlayerRead]]:
    player_repo = PlayerRepository(db=session)
    players = await player_repo.all(
        skip=skip, limit=limit, sort_field=sort_field, sort_order=sort_order
    )

    return IGetResponseBase[List[IPlayerRead]](data=players)


@router.get(
    "/player_by_league",
    response_description="List all players",
    response_model=IGetResponseBase[List[IPlayerRead]],
    tags=["players"],
)
async def list_player_by_league(
    league_id: UUID,
    sort_field: Optional[str] = "name",
    sort_order: Optional[str] = SortOrder.ASC,
    session: AsyncSession = Depends(get_session),
) -> IGetResponseBase[List[IPlayerRead]]:
    player_repo = PlayerRepository(db=session)
    players = await player_repo.all_by_league(
        sort_field=sort_field, sort_order=sort_order, league=league_id
    )

    return IGetResponseBase[List[IPlayerRead]](data=players)


@router.post(
    "/player",
    response_description="Add a new player",
    response_model=IPlayerRead,
    tags=["players"],
)
async def add_new_player(
    player: IPlayerCreate,
    session: AsyncSession = Depends(get_session),
) -> IPlayerRead:
    player_repo = PlayerRepository(db=session)
    new_player = await player_repo.create(player)

    return new_player


@router.put(
    "/player",
    response_description="Modify player",
    response_model=IPlayerRead,
    tags=["players"],
)
async def add_new_player(
    new_player: IPlayerUpdate,
    session: AsyncSession = Depends(get_session),
) -> IPlayerRead:
    player_repo = PlayerRepository(db=session)
    old_player = await player_repo.get(id=new_player.id)
    if not old_player:
        raise HTTPException(status_code=404, detail="Player not found")
    new_player = await player_repo.update(old_player, new_player)

    return new_player


@router.delete(
    "/player",
    response_description="Add a new player",
    tags=["players"],
)
async def delete_player(
    player_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> IPlayerRead:
    player_repo = PlayerRepository(db=session)
    try:
        await player_repo.delete(id=player_id)
        return JSONResponse(status_code=200, content={"message": f"Player {player_id} deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


