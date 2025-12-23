from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.report import MatchReportCreate, MatchReportOut
from app.services.match_report_service import (
    create_or_update_report,
    get_report_for_match_and_team,
    get_reports_for_match,
    get_reports_for_team,
)

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/matches/{match_id}/teams/{team_number}", response_model=MatchReportOut)
def create_or_update_match_team_report(
    match_id: int,
    team_number: int,
    payload: MatchReportCreate,
    db: Session = Depends(get_db),
):
    try:
        report = create_or_update_report(db, match_id=match_id, team_number=team_number, data=payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return report


@router.get("/matches/{match_id}/teams/{team_number}", response_model=MatchReportOut)
def get_match_team_report(
    match_id: int,
    team_number: int,
    db: Session = Depends(get_db),
):
    report = get_report_for_match_and_team(db, match_id=match_id, team_number=team_number)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.get("/matches/{match_id}", response_model=list[MatchReportOut])
def list_match_reports(match_id: int, db: Session = Depends(get_db)):
    return get_reports_for_match(db, match_id=match_id)


@router.get("/teams/{team_number}", response_model=list[MatchReportOut])
def list_team_reports(team_number: int, db: Session = Depends(get_db)):
    return get_reports_for_team(db, team_number=team_number)
