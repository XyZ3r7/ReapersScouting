
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.report import TeamReport
from app.schemas.report import TeamReportUpsert, TeamReportOut

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{team_number}", response_model=TeamReportOut)
def get_report(team_number: int, db: Session = Depends(get_db)):
    report = db.query(TeamReport).filter(TeamReport.team_number == team_number).one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="report_not_found")

    return TeamReportOut(
        team_number=report.team_number,
        shooting_range=report.shooting_range,
        robots_scored=report.robots_scored,
        max_score_without_pattern=report.max_score_without_pattern,
        max_score_with_pattern=report.max_score_with_pattern,
        needs_human_player=report.needs_human_player,
        has_lifting_for_parking=report.has_lifting_for_parking,
        notes=report.notes,
    )


@router.put("/{team_number}", response_model=TeamReportOut)
def upsert_report(team_number: int, payload: TeamReportUpsert, db: Session = Depends(get_db)):
    report = db.query(TeamReport).filter(TeamReport.team_number == team_number).one_or_none()
    if not report:
        report = TeamReport(team_number=team_number)
        db.add(report)

    # Update fields from payload
    for key, value in payload.model_dump().items():
        setattr(report, key, value)

    db.commit()
    db.refresh(report)

    return TeamReportOut(team_number=report.team_number, **payload.model_dump())
