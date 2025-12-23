from __future__ import annotations

from sqlalchemy import String, Integer, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class Team(Base):
    # __tablename__ = "teams"
    __tablename__ = "event_teams"

    team_number: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    city: Mapped[str | None] = mapped_column(String(128), nullable=True)
    state_prov: Mapped[str | None] = mapped_column(String(64), nullable=True)
    country: Mapped[str | None] = mapped_column(String(64), nullable=True)


class Event(Base):
    __tablename__ = "events"

    event_code: Mapped[str] = mapped_column(String(64), primary_key=True)
    season: Mapped[int] = mapped_column(Integer, index=True)
    name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    start_date: Mapped[str | None] = mapped_column(String(32), nullable=True)
    end_date: Mapped[str | None] = mapped_column(String(32), nullable=True)


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        UniqueConstraint("season", "event_code", "match_key", name="uq_match"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    season: Mapped[int] = mapped_column(Integer, index=True)
    event_code: Mapped[str] = mapped_column(String(64), index=True)

    match_key: Mapped[str] = mapped_column(String(64), index=True)
    match_type: Mapped[str | None] = mapped_column(String(32), nullable=True)
    start_time: Mapped[str | None] = mapped_column(String(64), nullable=True)

    red_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    blue_score: Mapped[int | None] = mapped_column(Integer, nullable=True)


class MatchParticipation(Base):
    __tablename__ = "match_participations"
    __table_args__ = (
        UniqueConstraint("match_id", "team_number", name="uq_match_team"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), index=True)
    team_number: Mapped[int] = mapped_column(Integer, index=True)

    alliance: Mapped[str | None] = mapped_column(String(8), nullable=True)  # "red"/"blue"
    station: Mapped[int | None] = mapped_column(Integer, nullable=True)     # 1/2

    score_detail_json: Mapped[str | None] = mapped_column(String, nullable=True)
