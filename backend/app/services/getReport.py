from __future__ import annotations

from rapidfuzz.fuzz import token_set_ratio
from sqlalchemy.orm import Session
from app.models.match import TeamReport
from app.core.config import settings

def _norm_text(s: str | None) -> str:
    return (s or "").strip()

def getReport(db: Session, team_id: int) -> str:
    report = db.query(TeamReport).filter(TeamReport.team_number == team_id).one_or_none();
    output = "";

    if not report:
        return "Team does not exist"
    robotName = "RobotName: " + report.robot_name
    drivetrain = "DriveTrain: " + report.drivetrain
    intakType = "IntakeType: " + report.intake_type
    cycleSpeed = "CycleSpeed: " + report.cycle_speed
    autoNotes = "Auto_notes:" + report.auto_notes
    strength = "Strength: " + report.strengths
    weakness = "Weakness: " + report.weaknesses
    notes = "Notes: " + report.notes

    return robotName + "\n" + drivetrain + "\n" + intakType + "\n" + cycleSpeed + "\n" + autoNotes + "\n" + strength + "\n" + weakness + "\n"
