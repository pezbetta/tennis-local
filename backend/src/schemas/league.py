from uuid import UUID

from src.models.league import LeagueBase


class ILeagueCreate(LeagueBase):
    pass


class ILeagueRead(LeagueBase):
    id: UUID


class ILeagueUpdate(LeagueBase):
    id: UUID