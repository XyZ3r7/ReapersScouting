from datetime import date, datetime
from pydantic import BaseModel


class MatchReportBase(BaseModel):
    match_date: date | None = None
    shooting_range: str | None = None
    robots_scored: int | None = None
    max_score_without_pattern: str | None = None
    max_score_with_pattern: str | None = None
    needs_human_player: str | None = None
    has_lifting_for_parking: str | None = None
    notes: str | None = None


class MatchReportCreate(MatchReportBase):
    pass


class MatchReportUpdate(MatchReportBase):
    pass


class MatchReportOut(MatchReportBase):
    id: int
    match_id: int
    team_id: int
    match_number: int | None = None
    created_at: datetime

    class Config:
        orm_mode = True
