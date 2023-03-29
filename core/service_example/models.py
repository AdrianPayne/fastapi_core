from sqlmodel import Field, Relationship
from typing import Optional
from pydantic import BaseModel

from core.models import ModelBase, ModelRecord


class RecordExample(ModelRecord, table=True):
    pass


class Team(ModelBase, table=True):
    _record_model = RecordExample

    name: str
    heroes: list["Hero"] = Relationship(back_populates="team", sa_relationship_kwargs={"lazy": "selectin"})


class HeroBase(BaseModel):
    name: str
    team_id: int | None = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, ModelBase, table=True):
    _record_model = RecordExample
    team: Optional[Team] = Relationship(back_populates="heroes", sa_relationship_kwargs={"lazy": "selectin"})
    secret_password: str
