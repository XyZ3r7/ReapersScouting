
from __future__ import annotations
from sqlalchemy import String, Integer, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class TeamReport(Base):
    __tablename__ = "team_reports"
    __table_args__ = (
        UniqueConstraint("team_number", name="uq_team_report"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_number: Mapped[int] = mapped_column(Integer, index=True)

    # New fields based on requirements
    shooting_range: Mapped[str] = mapped_column(String(32), nullable=False)  # near/far/mostly near/mostly far/varies
    robots_scored: Mapped[int] = mapped_column(Integer, nullable=False)      # integer >= 0
    max_score_without_pattern: Mapped[str] = mapped_column(String(32), nullable=False)  # int or "unknown"/"untested"
    max_score_with_pattern: Mapped[str] = mapped_column(String(32), nullable=False)     # int or "unknown"/"untested"
    needs_human_player: Mapped[str] = mapped_column(String(8), nullable=False)          # yes/no
    has_lifting_for_parking: Mapped[str] = mapped_column(String(8), nullable=False)     # yes/no
    notes: Mapped[str | None] = mapped_column(String(4000), nullable=True)              # free text

    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

