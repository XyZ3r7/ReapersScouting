from __future__ import annotations

from pydantic import BaseModel, Field


class TeamReportUpsert(BaseModel):
    robot_name: str | None = None
    drivetrain: str | None = Field(default=None, description="e.g. mecanum/tank/omni")
    intake_type: str | None = None
    cycle_speed: int | None = Field(default=None, ge=1, le=10)

    auto_notes: str | None = None
    strengths: str | None = None
    weaknesses: str | None = None
    notes: str | None = None


class TeamReportOut(TeamReportUpsert):
    team_number: int
