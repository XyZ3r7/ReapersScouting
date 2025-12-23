from datetime import datetime
from pydantic import BaseModel
from typing import List

from app.schemas.team import TeamOut


class MatchParticipationOut(BaseModel):
    id: int
    alliance: str | None
    station: int | None
    team: TeamOut

    class Config:
        orm_mode = True


class MatchBase(BaseModel):
    season: int
    event_code: str
    match_key: str
    match_number: int | None = None
    match_type: str | None = None
    start_time: datetime | None = None
    red_score: int | None = None
    blue_score: int | None = None


class MatchOut(MatchBase):
    id: int
    participations: List[MatchParticipationOut]

    class Config:
        orm_mode = True
