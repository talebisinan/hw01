from typing import List

from pydantic import BaseModel


class TeamBase(BaseModel):
    title: str
    description: str = None


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class WorkerBase(BaseModel):
    name: str


class Worker(WorkerBase):
    id: int
    teams: List[Team] = []

    class Config:
        orm_mode = True
