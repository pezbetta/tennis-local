from src.models.league import League
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from src.schemas.league import ILeagueCreate, ILeagueUpdate


class LeagueRepository(BaseSQLAlchemyRepository[League, ILeagueCreate, ILeagueUpdate]):
    _model = League