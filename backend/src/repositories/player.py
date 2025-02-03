from typing import List, Optional
from uuid import UUID
from src.models.player import Player
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from sqlmodel import select
from src.schemas.player import IPlayerCreate, IPlayerUpdate


class PlayerRepository(BaseSQLAlchemyRepository[Player, IPlayerCreate, IPlayerUpdate]):
    _model = Player

    async def all_by_league(
        self,
        league: UUID,
        skip: int = 0,
        limit: int = 100,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[Player]:
        columns = self._model.__table__.columns  # type: ignore

        if not sort_field:
            sort_field = "created_at"

        if not sort_order:
            sort_order = "desc"

        order_by = getattr(columns[sort_field], sort_order)()
        query = select(self._model).filter_by(league=league).offset(skip).limit(limit).order_by(order_by)

        response = await self.db.execute(query)
        return response.scalars().all()  # type: ignore