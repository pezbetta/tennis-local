from datetime import datetime
from uuid import UUID
from pydantic import BaseConfig
from sqlmodel import Field, SQLModel

from src.models.base import BaseModel

class MatchBase(SQLModel):
    player_1: UUID = Field(
        default=None, foreign_key="player.id"
    )
    player_2: UUID = Field(
        default=None, foreign_key="player.id"
    )
    date: datetime = Field(...)
    league: UUID = Field(
        default=None, foreign_key="league.id"
    )
    score: str | None = Field(default=None, nullable=True)
    winner: UUID | None = Field(
        default=None, foreign_key="player.id", nullable=True
    )

    class Config(BaseConfig):
        schema_extra = {
            "example": {
                "name": "Adnan Januzaj",
            }
        }

class Match(BaseModel, MatchBase, table=True):
    pass
