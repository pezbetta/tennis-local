from uuid import UUID
from pydantic import BaseConfig
from sqlmodel import Field, SQLModel

from src.models.base import BaseModel

class PlayerBase(SQLModel):
    name: str = Field(...)
    league: UUID = Field(
        default=None, foreign_key="league.id"
    )

    class Config(BaseConfig):
        schema_extra = {
            "example": {
                "name": "Adnan Januzaj",
            }
        }

class Player(BaseModel, PlayerBase, table=True):
    pass