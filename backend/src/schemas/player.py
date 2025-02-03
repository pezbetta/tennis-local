from uuid import UUID

from src.models.player import PlayerBase


class IPlayerCreate(PlayerBase):
    pass


class IPlayerRead(PlayerBase):
    id: UUID


class IPlayerUpdate(PlayerBase):
    id: UUID