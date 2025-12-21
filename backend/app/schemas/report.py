
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal, Union


class TeamReportUpsert(BaseModel):
    shooting_range: Literal["near", "far", "mostly near", "mostly far", "varies"] = Field(
        description="Is the shooting range near or far?"
    )

    robots_scored: int = Field(
        ge=0,
        description="Number of robots this robot can score"
    )

    max_score_without_pattern: Union[int, Literal["unknown", "untested"]] = Field(
        description="Maximum score without pattern (integer or unknown/untested)"
    )

    max_score_with_pattern: Union[int, Literal["unknown", "untested"]] = Field(
        description="Maximum score with pattern (integer or unknown/untested)"
    )

    needs_human_player: Literal["yes", "no"] = Field(
        description="Does the robot need a human player?"
    )

    has_lifting_for_parking: Literal["yes", "no"] = Field(
        description="Does the robot have lifting for parking?"
    )

    notes: str = Field(
        default="",
        description="Additional description about the robot"
    )


class TeamReportOut(TeamReportUpsert):
    team_number: int
