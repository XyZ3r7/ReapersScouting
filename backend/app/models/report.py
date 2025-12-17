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

    robot_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    drivetrain: Mapped[str | None] = mapped_column(String(64), nullable=True)
    intake_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    cycle_speed: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 1-10

    auto_notes: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    strengths: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    weaknesses: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(4000), nullable=True)

    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
