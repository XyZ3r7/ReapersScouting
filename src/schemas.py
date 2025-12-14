from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


# ===== Team =====

class TeamBase(BaseModel):
    team_number: int
    name: Optional[str] = None
    location: Optional[str] = None
    rookie_year: Optional[int] = None


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    rookie_year: Optional[int] = None


class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True


# ===== Review =====

class TeamReviewBase(BaseModel):
    reviewer: str
    auto_score: int
    teleop_score: int
    endgame_score: int
    defense_score: int
    reliability: int
    comment: Optional[str] = None


class TeamReviewCreate(TeamReviewBase):
    team_id: int


class TeamReview(TeamReviewBase):
    id: int
    team_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TeamWithReviews(Team):
    reviews: List[TeamReview] = []


# ===== Event =====

class EventBase(BaseModel):
    code: str
    name: str
    location: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int

    class Config:
        orm_mode = True


# ===== Similarity response =====

class TeamSimilarity(BaseModel):
    team: Team
    similarity: float
