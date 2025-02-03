from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from src.schemas.match import IMatchUpdate
from src.db.session import get_session
from src.repositories.match import MatchRepository
from src.core.enums import SortOrder
from src.schemas.common import IGetResponseBase
from src.schemas.match import IMatchRead, IMatchCreate

import logging
FORMAT = "%(levelname)s:%(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

logging.debug('This message should appear on the console')


router = APIRouter()


@router.get(
    "/match",
    response_description="List all matchs",
    response_model=IGetResponseBase[List[IMatchRead]],
    tags=["matchs"],
)
async def list_all_matchs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1),
    sort_field: Optional[str] = "id",
    sort_order: Optional[str] = SortOrder.DESC,
    session: AsyncSession = Depends(get_session),
) -> IGetResponseBase[List[IMatchRead]]:
    match_repo = MatchRepository(db=session)
    matchs = await match_repo.all(
        skip=skip, limit=limit, sort_field=sort_field, sort_order=sort_order
    )

    return IGetResponseBase[List[IMatchRead]](data=matchs)

@router.get(
    "/match_calendar",
    response_description="List all matchs",
    response_model=IGetResponseBase[List[IMatchRead]],
    tags=["matchs"],
)
async def list_match_calendar(
    league: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1),
    sort_field: Optional[str] = "id",
    sort_order: Optional[str] = SortOrder.DESC,
    session: AsyncSession = Depends(get_session),
) -> IGetResponseBase[List[IMatchRead]]:
    match_repo = MatchRepository(db=session)
    matchs = await match_repo.all(
        skip=skip, limit=limit, sort_field=sort_field, sort_order=sort_order
    )

    return IGetResponseBase[List[IMatchRead]](data=matchs)


@router.post(
    "/match",
    response_description="Add a new match",
    response_model=IMatchRead,
    tags=["matchs"],
)
async def add_new_match(
    match: IMatchCreate,
    session: AsyncSession = Depends(get_session),
) -> IMatchRead:
    match_repo = MatchRepository(db=session)
    new_match = await match_repo.create(match)

    return new_match


@router.put(
    "/match",
    response_description="Modify match",
    response_model=IMatchRead,
    tags=["matchs"],
)
async def add_new_match(
    new_match: IMatchUpdate,
    session: AsyncSession = Depends(get_session),
) -> IMatchRead:
    match_repo = MatchRepository(db=session)
    old_match = await match_repo.get(id=new_match.id)
    if not old_match:
        raise HTTPException(status_code=404, detail="Match not found")
    new_match = await match_repo.update(old_match, new_match)

    return new_match


@router.delete(
    "/match",
    response_description="Add a new match",
    tags=["matchs"],
)
async def delete_match(
    match_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> IMatchRead:
    match_repo = MatchRepository(db=session)
    try:
        await match_repo.delete(id=match_id)
        return JSONResponse(status_code=200, content={"message": f"Match {match_id} deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


