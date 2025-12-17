from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.report import TeamReport
from app.schemas.report import TeamReportUpsert, TeamReportOut

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{team_number}", response_model=TeamReportOut)
def get_report(team_number: int, db: Session = Depends(get_db)):
    r = db.query(TeamReport).filter(TeamReport.team_number == team_number).one_or_none()
    if not r:
        raise HTTPException(status_code=404, detail="report_not_found")
    return TeamReportOut(
        team_number=r.team_number,
        robot_name=r.robot_name,
        drivetrain=r.drivetrain,
        intake_type=r.intake_type,
        cycle_speed=r.cycle_speed,
        auto_notes=r.auto_notes,
        strengths=r.strengths,
        weaknesses=r.weaknesses,
        notes=r.notes,
    )


@router.put("/{team_number}", response_model=TeamReportOut)
def upsert_report(team_number: int, payload: TeamReportUpsert, db: Session = Depends(get_db)):
    r = db.query(TeamReport).filter(TeamReport.team_number == team_number).one_or_none()
    if not r:
        r = TeamReport(team_number=team_number)
        db.add(r)

    for k, v in payload.model_dump().items():
        setattr(r, k, v)

    db.commit()
    db.refresh(r)
    return TeamReportOut(team_number=r.team_number, **payload.model_dump())
