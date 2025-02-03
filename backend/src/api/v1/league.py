from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.schemas.league import ILeagueUpdate
from src.db.session import get_session
from src.repositories.league import LeagueRepository
from src.core.enums import SortOrder
from src.schemas.common import IGetResponseBase
from src.schemas.league import ILeagueRead, ILeagueCreate

import logging
FORMAT = "%(levelname)s:%(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

logging.debug('This message should appear on the console')


router = APIRouter()


@router.get(
    "/league",
    response_description="List all leagues",
    response_model=IGetResponseBase[List[ILeagueRead]],
    tags=["leagues"],
)
async def list_all_leagues(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1),
    sort_field: Optional[str] = "id",
    sort_order: Optional[str] = SortOrder.DESC,
    session: AsyncSession = Depends(get_session),
) -> IGetResponseBase[List[ILeagueRead]]:
    league_repo = LeagueRepository(db=session)
    leagues = await league_repo.all(
        skip=skip, limit=limit, sort_field=sort_field, sort_order=sort_order
    )

    return IGetResponseBase[List[ILeagueRead]](data=leagues)


@router.post(
    "/league",
    response_description="Add a new league",
    response_model=ILeagueRead,
    tags=["leagues"],
)
async def add_new_league(
    league: ILeagueCreate,
    session: AsyncSession = Depends(get_session),
) -> ILeagueRead:
    league_repo = LeagueRepository(db=session)
    new_league = await league_repo.create(league)

    return new_league


@router.put(
    "/league",
    response_description="Modify league",
    response_model=ILeagueRead,
    tags=["leagues"],
)
async def add_new_league(
    new_league: ILeagueUpdate,
    session: AsyncSession = Depends(get_session),
) -> ILeagueRead:
    league_repo = LeagueRepository(db=session)
    old_league = await league_repo.get(id=new_league.id)
    if not old_league:
        raise HTTPException(status_code=404, detail="League not found")
    new_league = await league_repo.update(old_league, new_league)

    return new_league


@router.delete(
    "/league",
    response_description="Add a new league",
    tags=["leagues"],
)
async def delete_league(
    league_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> ILeagueRead:
    league_repo = LeagueRepository(db=session)
    try:
        await league_repo.delete(id=league_id)
        return JSONResponse(status_code=200, content={"message": f"League {league_id} deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


