from datetime import datetime
from typing import List, Optional
from uuid import UUID
from src.models.match import Match
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from src.schemas.match import IMatchCreate, IMatchUpdate
from sqlmodel import select


class MatchRepository(BaseSQLAlchemyRepository[Match, IMatchCreate, IMatchUpdate]):
    _model = Match

    async def all_by_league(
        self,
        league: UUID,
        date: datetime,
        skip: int = 0,
        limit: int = 100,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[Match]:
        columns = self._model.__table__.columns  # type: ignore

        if not sort_field:
            sort_field = "created_at"

        if not sort_order:
            sort_order = "desc"

        order_by = getattr(columns[sort_field], sort_order)()
        query = select(self._model).filter(self._model.date >= date).filter_by(league=league).offset(skip).limit(limit).order_by(order_by)

        response = await self.db.execute(query)
        return response.scalars().all()  # type: ignore