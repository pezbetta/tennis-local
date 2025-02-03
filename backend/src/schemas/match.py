from uuid import UUID

from src.models.match import MatchBase


class IMatchCreate(MatchBase):
    pass


class IMatchRead(MatchBase):
    id: UUID


class IMatchUpdate(MatchBase):
    id: UUID