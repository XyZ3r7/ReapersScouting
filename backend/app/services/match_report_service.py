from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.team import Team
from app.models.match_report import MatchReport
from app.schemas.report import MatchReportCreate, MatchReportUpdate


def get_or_create_team(db: Session, team_number: int) -> Team:
    team = db.query(Team).filter(Team.team_number == team_number).one_or_none()
    if not team:
        team = Team(team_number=team_number, from_event_sync=False)
        db.add(team)
        db.commit()
        db.refresh(team)
    return team


def get_match_by_id(db: Session, match_id: int) -> Match | None:
    return db.query(Match).filter(Match.id == match_id).one_or_none()


def get_or_create_report(db: Session, match_id: int, team_id: int) -> MatchReport:
    report = (
        db.query(MatchReport)
        .filter(MatchReport.match_id == match_id, MatchReport.team_id == team_id)
        .one_or_none()
    )
    if not report:
        report = MatchReport(match_id=match_id, team_id=team_id)
        db.add(report)
        db.commit()
        db.refresh(report)
    return report


def create_or_update_report(
    db: Session,
    match_id: int,
    team_number: int,
    data: MatchReportCreate,
) -> MatchReport:
    match = get_match_by_id(db, match_id)
    if not match:
        raise ValueError("Match not found")

    team = get_or_create_team(db, team_number)
    report = get_or_create_report(db, match_id=match.id, team_id=team.id)

    report.match_number = match.match_number
    report.match_date = data.match_date or (match.start_time.date() if match.start_time else date.today())
    report.shooting_range = data.shooting_range
    report.robots_scored = data.robots_scored
    report.max_score_without_pattern = data.max_score_without_pattern
    report.max_score_with_pattern = data.max_score_with_pattern
    report.needs_human_player = data.needs_human_player
    report.has_lifting_for_parking = data.has_lifting_for_parking
    report.notes = data.notes

    db.commit()
    db.refresh(report)
    return report


def get_report_for_match_and_team(db: Session, match_id: int, team_number: int) -> MatchReport | None:
    team = db.query(Team).filter(Team.team_number == team_number).one_or_none()
    if not team:
        return None
    return (
        db.query(MatchReport)
        .filter(MatchReport.match_id == match_id, MatchReport.team_id == team.id)
        .one_or_none()
    )


def get_reports_for_match(db: Session, match_id: int) -> list[MatchReport]:
    return db.query(MatchReport).filter(MatchReport.match_id == match_id).all()


def get_reports_for_team(db: Session, team_number: int) -> list[MatchReport]:
    team = db.query(Team).filter(Team.team_number == team_number).one_or_none()
    if not team:
        return []
    return db.query(MatchReport).filter(MatchReport.team_id == team.id).all()
