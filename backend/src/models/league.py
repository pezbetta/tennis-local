from datetime import datetime
from pydantic import BaseConfig
from sqlmodel import Field, SQLModel

from src.models.base import BaseModel

class LeagueBase(SQLModel):
    name: str = Field(...)
    active: bool = Field(default=True)
    finish_on: datetime | None = Field(default=None, nullable=True)
    start_on: datetime | None = Field(default=None, nullable=True)
    description: str | None = Field(default=None, nullable=True)

    class Config(BaseConfig):
        schema_extra = {
            "example": {
                "name": "Ciudad Real League",
            }
        }

class League(BaseModel, LeagueBase, table=True):
    pass